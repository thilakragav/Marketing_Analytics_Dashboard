from sql_generator import generate_sql


questions = [
    "How many records are in the Google Search Console data?",
    "What is the total number of clicks?",
    "Which search query has the highest number of clicks?",
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)

    sql = generate_sql(question)

    print("\nGENERATED SQL:")
    print(sql)