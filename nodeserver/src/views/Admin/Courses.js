// Chakra imports
import {
  useColorModeValue,
  Flex,
  Text,
  Box,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionIcon,
  AccordionPanel,
} from "@chakra-ui/react";

// Custom components
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardHeader from "components/Card/CardHeader.js";
import CourseForm from "components/Forms/courseForm";
import React, { useEffect, useState } from "react";
import CourseListFilter from "components/Filter/CourseListFilter";
import { useDispatch, useSelector } from "react-redux";
import { courseListAction } from "redux/course/courseList/courseListAction";
import CourseListTable from "components/Tables/CourseListTable/CourseListTable";
import AuthorizeProvider from "helpers/authorize/AuthorizeProvider";
import { CoursePop1 } from "components/PopOvers/CoursePopOver";
import { getCourseBySearch } from "services/course";
import { deleteCourse } from "services/course";
import { getCourseListLimited } from "services/course";
import { getUserByRole } from "services/user";
import useNotify from "helpers/notify/useNotify";

function Courses() {
  const textColor = useColorModeValue("gray.700", "white");
  const boxBg = useColorModeValue("gray.100", "navy.600");

  const statusData = [
    { _id: "active", name: "فعال" },
    { _id: "deactive", name: "غیرفعال" },
  ];

  const { courseList } = useSelector((state) => state.courseList);

  const [state, setState] = useState([]);
  const [teachers, setTeachers] = useState([]);

  const callData = async () => {
    await getCourseListLimited().then((res) => {
      setState(res.data.data);
    });

    await getUserByRole("teacher").then((res) => {
      setTeachers(res.data.data);
    });
  };

  const [filter, setFilter] = React.useState({
    fFullName: "",
    fTeacher: {
      id: "",
      name: "",
    },
    fStatus: {
      id: "",
      name: "",
    },
  });
  const notify = useNotify();
  const handleDelete = (_id) => {
    deleteCourse(_id).then((res) => {
      if (res.status === 200) {
        setState(state.filter((course) => course._id !== res.data.data));
      } else if (res.status === 422) {
        if (res.data.detail.result === "has_product") {
          notify(
            "این دوره برای محصولاتی تعریف شده و قابل حذف نمی باشد",
            true,
            "solid",
            "error"
          );
        } else if (res.data.detail.result === "has_user") {
          notify(
            "این دوره برای کاربرانی تعریف شده و قابل حذف نمی باشد",
            true,
            "solid",
            "error"
          );
        }
      }
    });
  };

  const handleChange = (e) => {
    const field = e.target.id;
    const value = e.target.value;
    setFilter({ ...filter, [field]: value });
  };

  const doSearch = async () => {
    await getCourseBySearch(filter).then((res) => {
      setState(res.data.data);
    });
  };

  useEffect(() => {
    if (
      filter.fTeacher.id !== "" ||
      filter.fFullName !== "" ||
      filter.fStatus.id !== ""
    ) {
      doSearch();
    }
  }, [filter.fTeacher, filter.fFullName, filter.fStatus]);

  useEffect(() => {
    callData();
  }, []);

  return (
    <AuthorizeProvider roles={["admin"]}>
      <Flex direction="column" pt="75px">
        <Card overflowX={{ sm: "scroll", xl: "hidden" }} 
        overflowY={'hidden'} pb="20px">
          <Accordion defaultIndex={[1]} allowMultiple>
            <AccordionItem>
              <AccordionButton>
                <CoursePop1 />

                <Box
                  fontWeight={"bold"}
                  fontSize={"20px"}
                  as="span"
                  flex="1"
                  textAlign="right"
                >
                  ثبت دوره جدید
                </Box>

                <AccordionIcon />
              </AccordionButton>

              <AccordionPanel pb={4}>
                <CardBody>
                  <CourseForm
                    courses={courseList}
                    statusData={statusData}
                    callData={callData}
                  />
                </CardBody>
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
        </Card>
        <Card my="22px" overflowX={{ sm: "scroll", xl: "hidden" }} pb="0px">
          <CardHeader p="6px 0px 22px 0px">
            <CourseListFilter
              filter={filter}
              onChange={handleChange}
              courses={courseList}
              selectChange={setFilter}
              courseStatus={statusData}
              teacher={teachers ? teachers : []}
            />
          </CardHeader>

          {state.length !== 0 ? (
            <CourseListTable
              handleDelete={handleDelete}
              statusData={statusData}
              data={state}
              courses={courseList}
              callData={callData}
            />
          ) : (
            <Box
              mb={"30px"}
              borderRadius={"3rem"}
              alignSelf={"center"}
              width={{ sm: "300px", md: "500px", lg: "500px" }}
              bg={boxBg}
            >
              <Text textAlign={"center"} my={"10px"}>
                دوره ای یافت نشد
              </Text>
            </Box>
          )}
        </Card>
      </Flex>
    </AuthorizeProvider>
  );
}

export default Courses;
