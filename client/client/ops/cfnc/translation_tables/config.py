tt_job_config = {
    "ops": {
        "cfnc_translation_tables_update_graph": {
            "ops": {
                "sync_genders_translation_table_cfnc": {
                    "ops": {
                        "update_genders_translation_in_mongo_op": {
                            "config": {"data_source_type": "genders"}
                        }
                    }
                },
                "sync_majors_translation_table_cfnc": {
                    "ops": {
                        "get_element_majors_op": {
                            "config": {"data_source_collection": "luminous_majors"}
                        },
                        "update_majors_translation_in_mongo_op": {
                            "config": {"data_source_type": "majors"}
                        },
                    }
                },
                "sync_races_translation_table_cfnc": {
                    "ops": {
                        "update_races_translation_in_mongo_op": {
                            "config": {"data_source_type": "races"}
                        },
                    }
                },
                "sync_terms_translation_table_cfnc": {
                    "ops": {
                        "get_element_terms_op": {
                            "config": {"data_source_collection": "luminous_terms"}
                        },
                        "update_terms_translation_in_mongo_op": {
                            "config": {"data_source_type": "terms"}
                        },
                    }
                },
                "sync_student_types_translation_table_cfnc": {
                    "ops": {
                        "update_student_types_translation_in_mongo_op": {
                            "config": {"data_source_type": "student_types"}
                        },
                    }
                },
                "sync_academic_loads_translation_table_cfnc": {
                    "ops": {
                        "get_element_academic_loads_op": {
                            "config": {"data_source_guid": "data_source.academic_load"}
                        },
                        "update_academic_loads_translation_in_mongo_op": {
                            "config": {"data_source_type": "academic_loads"}
                        },
                    }
                },
                "sync_citizenship_statuses_translation_table_cfnc": {
                    "ops": {
                        "get_element_citizenship_statuses_op": {
                            "config": {"data_source_guid": "data_source.citizenship"}
                        },
                        "update_citizenship_statuses_translation_in_mongo_op": {
                            "config": {"data_source_type": "citizenship_statuses"}
                        },
                    }
                },
                # "sync_educational_level_translation_table_cfnc": {
                #     "ops": {
                #         "get_element_educational_level_op": {
                #             "config": {
                #                 "data_source_guid": ""
                #             }  # TODO: add data source guid
                #         },
                #         "update_educational_level_translation_in_mongo_op": {
                #             "config": {"data_source_type": "educational_levels"}
                #         },
                #     }
                # },
            }
        }
    },
    "resources": {"values": {"config": {"other_system": "cfnc"}}},
}
