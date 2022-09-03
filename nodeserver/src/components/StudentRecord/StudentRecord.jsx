import { DocumentIcon } from "components/Icons/Icons";
import {
  Avatar,
  Divider,
  Flex,
  Stat,
  StatLabel,
  StatNumber,
  Text,
  Spacer,
  Box,
  useColorMode,
  Grid,
  Badge,
  useDisclosure,
  GridItem,
  SimpleGrid,
  Modal,
  ModalOverlay,
  ModalContent,  
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";
import React, { useEffect } from "react";

import Card from "components/Card/Card";
import IconBox from "components/Icons/IconBox";
import { StarIcon } from "@chakra-ui/icons";
import MarkEditModal from "components/Modal/MarkEdit";
// onClick={()=>handleStudentSelect(_id, full_name)}
const StudentRecord = ({ studentRecord , handleStudentSelect }) => {
  const { full_name , _id } = studentRecord;

    
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const initialRef = React.useRef(null);
  const finalRef = React.useRef(null);


const handleOpenCard = ()=>{


  handleStudentSelect(_id, full_name)
  onOpen()



}
  

  const { colorMode } = useColorMode();

  return (
    <div className="record-card" onClick={handleOpenCard} >
<SimpleGrid   w={{ sm: "180px", md: "250px", lg: "320px" }}
        h="120px"
        borderWidth="1px"
        borderRadius="2rem"
        overflow="hidden"
        bg={colorMode === "light" ? "white" : "navy.700"}
        _hover={colorMode === "light" ? 
        {
          background: "gray.200",
          color: "black",
          transition:"0.5s"
        }
      :
      {
        background: "navy.300",
        color: "navy.600",
        transition:"0.5s"
      }
      } spacing={0} columns={3}>
  <Box   >
    

<Avatar
          my={"20px"}
          ml={"10px"}
          size="lg"
          name="Prosper Otemuyiwa"
          src="https://bit.ly/prosper-baba"
        />
  </Box>


  <Box  textAlign={"center"}>
    <Text fontFamily={"Lalezar"} pt={"5px"} fontSize={"xl"}>این یک تست برای </Text>
    <Divider />
    <Text textAlign={"center"} fontSize={"sm"} >family friends</Text>
    <Badge colorScheme='purple'>New</Badge>
    <Text fontSize={"sm"}>معدل کل : 98.5</Text>


  </Box>

</SimpleGrid>

<Modal
          size={"5xl"}
          initialFocusRef={initialRef}
          finalFocusRef={finalRef}
          isOpen={isOpen}
          onClose={onClose}
        >
          <ModalOverlay />
          <ModalContent>
            <ModalCloseButton />
            <ModalBody pt={"50px"}>
        



        
            </ModalBody>
          </ModalContent>
        </Modal>



    </div>
  );
};
export default StudentRecord;