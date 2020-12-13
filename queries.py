from datetime import date, timedelta

def benchmark_date(years):
    return (date.today() - timedelta(days = years * 365.25)).strftime('%Y-%m-%d')


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

BABY_GRANT_QUERY = """
                        SELECT household_id, dob
                        FROM members
                        WHERE dob > '{}'

                    """.format(benchmark_date(5))

ELDER_BONUS_QUERY = """
                        SELECT
                            t1.household_id, t1.dob, t2.type
                        FROM members t1
                        LEFT JOIN households t2
                        ON t1.household_id = t2.id
                        WHERE t2.type == 'HDB' AND t1.dob < '{}'

                    """.format(benchmark_date(50))

STUDENT_BONUS_QUERY = """
                        SELECT
                            household_id, SUM(annual_income) AS total_income, dob
                        FROM members
                        GROUP BY household_id
                        HAVING dob > '{}' AND total_income < 150000

                        """.format(benchmark_date(16))

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
