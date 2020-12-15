from datetime import date, timedelta

def benchmark_date(years):
    return (date.today() - timedelta(days = years * 365.25)).strftime('%Y-%m-%d')


STUDENT_BONUS_QUERY = """
                        SELECT
                            t1.household_id, t1.total_income, t2.dob
                        FROM (
                            SELECT
                                household_id, SUM(annual_income) AS total_income
                            FROM members
                            GROUP BY household_id
                            ) AS t1
                        INNER JOIN members t2
                        ON t1.household_id = t2.household_id
                        WHERE t2.dob > '{}' AND t1.total_income < 150000
                        """.format(benchmark_date(16))


FAMILY_SCHEME_QUERY = """
                        SELECT
                            t1.household_id, t1.id, t1.spouse_id
                        FROM members t1
                        INNER JOIN members t2
                        ON t1.household_id = t2.household_id AND t1.id = t2.spouse_id AND t1.spouse_id = t2.id
                        INNER JOIN members t3
                        ON t2.household_id = t3.household_id
                        WHERE t3.dob > '{}'

                    """.format(benchmark_date(18))

ELDER_BONUS_QUERY = """
                        SELECT
                            t1.household_id, t1.dob, t2.type
                        FROM members t1
                        LEFT JOIN households t2
                        ON t1.household_id = t2.id
                        WHERE t2.type == 'HDB' AND t1.dob < '{}'

                    """.format(benchmark_date(50))


BABY_GRANT_QUERY = """
                        SELECT household_id, dob
                        FROM members
                        WHERE dob > '{}'

                    """.format(benchmark_date(5))


YOLO_GRANT_QUERY = """
                        SELECT
                            t1.household_id, t1.total_income, t2.type
                        FROM (
                            SELECT
                                household_id, SUM(annual_income) AS total_income
                            FROM members
                            GROUP BY household_id
                            ) AS t1
                        LEFT JOIN households t2
                        ON t1.household_id = t2.id
                        WHERE t2.type == "HDB" AND t1.total_income < 100000

                        """


MANUAL_QUERY = """
                    SELECT
                        t1.household_id, t1.total_income, t1.household_size, t2.type
                    FROM (
                        SELECT
                            household_id, SUM(annual_income) AS total_income, COUNT(*) AS household_size
                        FROM members
                        GROUP BY household_id
                        ) AS t1
                    LEFT JOIN households t2
                    ON t1.household_id = t2.id
                    WHERE t2.type IN ('{housing_type}') AND t1.total_income <= {max_total_income} AND t1.household_size <= {max_household_size}

                """
