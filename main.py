from loaders.data_loader import load_data
from embeddings.embedding import EmbeddingModel
from vectordb.vector_store import VectorStore
from retriever.retriever import Retriever

# Load data
documents = load_data()

# Embeddings
embed_model = EmbeddingModel()
texts = [doc.page_content for doc in documents]
embeddings = embed_model.get_embeddings(texts)

# Vector DB
vector_db = VectorStore()
vector_db.add_documents(documents, embeddings)

# Retriever
retriever = Retriever(vector_db.collection, embed_model)


# 🔥 FINAL ANSWER FUNCTION
def final_answer(query):

    results = retriever.query(query)

    students = []

    # Convert text → dict
    for doc in results["documents"][0]:
        data = {}
        for line in doc.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                data[key.strip()] = value.strip()

        if "id" in data:
            students.append(data)

    query_lower = query.lower()

    # ✅ HOW MANY COURSES
    if "how many course" in query_lower or "how many courses" in query_lower:
        courses = set()
        for doc in documents:
            for line in doc.page_content.split("\n"):
                if "course" in line:
                    courses.add(line.split(": ")[1])
        return f"Total courses: {len(courses)}"

    # ✅ HOW MANY STUDENTS
    elif "how many" in query_lower:
        return f"Total students: {len(documents)}"

    # ✅ FILTER COURSE
    if "cs" in query_lower:
        students = [s for s in students if s.get("course", "").lower() == "cs"]

    if "it" in query_lower:
        students = [s for s in students if s.get("course", "").lower() == "it"]

    # ✅ FILTER MARKS ABOVE
    if "above" in query_lower:
        try:
            value = int(query_lower.split("above ")[1].split()[0])
            students = [s for s in students if int(s.get("marks", 0)) > value]
        except:
            pass

    # ✅ FILTER MARKS BELOW
    if "below" in query_lower:
        try:
            value = int(query_lower.split("below ")[1].split()[0])
            students = [s for s in students if int(s.get("marks", 0)) < value]
        except:
            pass

    # ✅ SORT (highest marks first)
    students = sorted(students, key=lambda x: int(x.get("marks", 0)), reverse=True)

    # ✅ TOP STUDENT
    if "top student" in query_lower or "best student" in query_lower:
        if students:
            s = students[0]
            return f"Top Student: {s['name']} ({s['course']}) - {s['marks']} marks"
        else:
            return "No student found"

    # ✅ OUTPUT
    if not students:
        return "No students found"

    answer = "\nTop Students:\n"
    for s in students[:5]:
        answer += f"{s['name']} ({s['course']}) - {s['marks']} marks\n"

    return answer


# 🔥 CONSOLE LOOP
while True:
    query = input("\nAsk question (type exit): ")

    if query.lower() == "exit":
        print("\nThank you for using Student Query System 😊")
        print("Goodbye 👋")
        break

    print("\nAnswer:\n")
    print(final_answer(query))