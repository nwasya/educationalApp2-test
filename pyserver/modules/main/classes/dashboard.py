from pymongo.database import Database, Collection
from modules.main.sonay_app import sn
from bson import ObjectId
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
from datetime import datetime


class SDashboard:
    database: str = "database"
    course_collection: str = 'course'
    user_collection: str = 's_user'

    def __init__(self, database, course_collection, user_collection, mark_collection, purchase_collection):
        self.database = database
        self.course_collection = course_collection
        self.user_collection = user_collection
        self.mark_collection = mark_collection
        self.purchase_collection = purchase_collection

    def get_counts(self):
        db: Database = sn.databases[self.database].db
        col: Collection = db[self.user_collection]
        col1: Collection = db[self.purchase_collection]
        col2: Collection = db[self.course_collection]
        current_date = datetime.today()

        # Subtract 20 months from current date

        one_month_ago = current_date - relativedelta(months=1)
        two_month_ago = current_date - relativedelta(months=2)
        itm_ready = {
            'students': {
                "count": 0,
                "perc": 0
            },
            'teachers': {
                "count": 0,
                "perc": 0
            },
            'purchases': {
                "count": 0,
                "perc": 0
            },
            'courses': {
                "count": 0,
                "perc": 0
            },
        }
        students = list(col.aggregate([
            {
                '$facet': {
                    'this_month': [
                        {
                            '$match': {'created': {'$gte': one_month_ago},
                                       'roles.id': 'student'}

                        },
                        {
                            "$set": {'key': 1}
                        },

                        {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ],
                    'last_month': [
                        {
                            '$match': {"$and":
                                       [
                                           {'created': {'$gte': two_month_ago}},
                                           {'created': {'$lt': one_month_ago}},
                                           {'roles.id': 'student'}
                                       ]
                                       }

                        },
                        {
                            "$set": {'key': 1}
                        }, {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ],
                    'total': [{
                        '$match': {'roles.id': 'student'}
                    },

                        {
                        "$set": {'key': 1}
                    },
                        {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                    },

                    ]

                }
            }
        ]))

        teachers = list(col.aggregate([
            {
                '$facet': {
                    'this_month': [
                        {
                            '$match': {'created': {'$gte': one_month_ago},
                                       'roles.id': 'teacher'}

                        },
                        {
                            "$set": {'key': 1}
                        },

                        {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ],
                    'last_month': [
                        {
                            '$match': {"$and":
                                       [
                                           {'created': {'$gte': two_month_ago}},
                                           {'created': {'$lt': one_month_ago}},
                                           {'roles.id': 'teacher'}
                                       ]
                                       }

                        },
                        {
                            "$set": {'key': 1}
                        }, {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ],
                    'total': [{
                        '$match': {'roles.id': 'teacher'}
                    },

                        {
                        "$set": {'key': 1}
                    },
                        {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                    },

                    ]

                }
            }
        ]))

        purchases = list(col1.aggregate([
            {
                '$facet': {
                    'this_month': [
                        {
                            '$match': {
                                'g_date': {"$gte": one_month_ago},
                                'type': {
                                    '$ne': 'pending'
                                }
                            }
                        }, {
                            '$set': {
                                'key': 1
                            }
                        }, {
                            '$group': {
                                '_id': '$key',
                                'sum': {
                                    '$sum': '$price'
                                }
                            }
                        }
                    ],
                    'last_month': [
                        {
                            '$match': {

                                "$and":
                                [
                                    {'g_date': {'$gte': two_month_ago}},
                                    {'g_date': {'$lt': one_month_ago}},
                                    {'type': {'$ne': 'pending'}}
                                ]


                            }
                        }, {
                            '$set': {
                                'key': 1
                            }
                        }, {
                            '$group': {
                                '_id': '$key',
                                'sum': {
                                    '$sum': '$price'
                                }
                            }
                        }
                    ],

                }
            }
        ])
        )

        courses = list(col2.aggregate([
            {
                '$facet': {
                    'this_month': [
                        {
                            '$match': {
                                'g_date': {"$gte": one_month_ago},
                                'status.id': 'active'
                            }
                        }, {
                            '$set': {
                                'key': 1
                            }
                        }, {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ],
                    'last_month': [
                        {
                            '$match': {
                                "$and":
                                [
                                    {'g_date': {'$gte': two_month_ago}},
                                    {'g_date': {'$lt': one_month_ago}},
                                    {'status.id': 'active'}
                                ]

                            }
                        }, {
                            '$set': {
                                'key': 1
                            }
                        }, {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ],
                    'total': [
                        {
                            '$match': {
                                "$and":
                                [

                                    {'status.id': 'active'}
                                ]

                            }
                        }, {
                            '$set': {
                                'key': 1
                            }
                        }, {
                            '$group': {
                                '_id': '$key',
                                'count': {
                                    '$count': {}
                                }
                            }
                        }
                    ]
                }
            }
        ]))

        res = self.prepare_count_data(
            students, teachers, purchases, courses, itm_ready)
        return 200, "ok", "course is inserted", [res]

    def calculate_percantage(self, first_value, sec_value):
        if first_value == 0:
            return 100
        return ((sec_value - first_value) / first_value)*100

    def prepare_count_data(self, students, teachers, purchases, courses, template):
        template['students']['count'] = 0 if len(
            students[0]['total']) == 0 else students[0]['total'][0]['count']
        template['students']['perc'] = self.calculate_percantage(
            self.get_per_month_data(students[0]['last_month'], 'count'),
            self.get_per_month_data(students[0]['this_month'], 'count')
        )

        template['teachers']['count'] = 0 if len(
            teachers[0]['total']) == 0 else teachers[0]['total'][0]['count']
        template['teachers']['perc'] = self.calculate_percantage(
            self.get_per_month_data(teachers[0]['last_month'], 'count'),
            self.get_per_month_data(teachers[0]['this_month'], 'count')
        )

        template['purchases']['count'] = 0 if len(
            purchases[0]['this_month']) == 0 else purchases[0]['this_month'][0]['sum']
        template['purchases']['perc'] = self.calculate_percantage(
            self.get_per_month_data(purchases[0]['last_month'], 'sum'),
            self.get_per_month_data(purchases[0]['this_month'], 'sum')
        )

        template['courses']['count'] = 0 if len(
            courses[0]['total']) == 0 else courses[0]['total'][0]['count']
        template['courses']['perc'] = self.calculate_percantage(
            self.get_per_month_data(courses[0]['last_month'], 'count'),
            self.get_per_month_data(courses[0]['this_month'], 'count')
        )

        return template

    def get_per_month_data(self, data: list, field):
        if len(data) == 0:
            return 0
        else:
            return data[0][field]

    def get_year_compare_data(self):
        db: Database = sn.databases[self.database].db
        col: Collection = db[self.purchase_collection]
        current_year = datetime.today().year
        data = list(col.aggregate([

            {
                '$facet': {
                    'this_year': [
                        {
                            '$match': {
                                'y': {
                                    '$eq': 1401
                                }
                            }
                        }, {
                            '$group': {
                                '_id': "$m",
                                'sum': {
                                    '$sum': '$price'
                                }
                            }
                        }
                    ],
                    'last_year': [
                        {
                            '$match': {
                                'y': {
                                    '$eq': 1400
                                }
                            }
                        }, {
                            '$group': {
                                '_id': "$m",
                                'sum': {
                                    '$sum': '$price'
                                }
                            }
                        }
                    ]
                }
            }
        ])
        )
        res = self.prepare_year_compare_data(data)
        return 200, "ok", "course is inserted", res

    def prepare_year_compare_data(self, data):

        itm_ready_this_year = {1: 0, 2: 0, 3: 0, 4: 0,
                               5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        itm_ready_last_year = {1: 0, 2: 0, 3: 0, 4: 0,
                               5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

        for itm in data[0]['this_year']:
            itm_ready_this_year[itm['_id']] = itm['sum']

        for itm in data[0]['last_year']:
            itm_ready_last_year[itm['_id']] = itm['sum']

        return [
            {'name': 'امسال',
             'data': list(itm_ready_this_year.values())},
            {'name': 'سال قبل',
             'data': list(itm_ready_last_year.values())}
        ]

    def get_teacher_overall(self):
        db: Database = sn.databases[self.database].db
        col: Collection = db[self.mark_collection]
        data = list(col.aggregate([
            {
                '$group': {
                    '_id': '$teacher',
                    'avg': {
                        '$avg': '$sum'
                    }
                }
            }, {
                '$project': {
                    'avg': {
                        '$round': [
                            '$avg', 2
                        ]
                    },
                    'name': '$_id.name',
                    '_id' : 0
                }
            }
        ]))
        
        return 200, "ok", "course is inserted", data
        
