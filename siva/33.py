students = [
     {"name": "siva", "attendance": 45, "marks": [67, 89, 56]},
     {"name": "mani", "attendance": 67, "marks": [45, 23, 56]},
     {"name": "isha", "attendance": 89, "marks": [90, 85, 88]},
     {"name": "sravani", "attendance": 23, "marks": [40, 35, 30]},
     {"name": "pandu", "attendance": 56, "marks": [70, 65, 60]}
 ]


def classify_student(student):
    total = 0
    for m in student["marks"]:
        total += m
    avg_marks = total / len(student["marks"])

    att = student["attendance"]

    if att >= 75 and avg_marks >= 75:
        label = "Excellent"
    elif att >= 50 and avg_marks >= 50:
        label = "On Track"
    elif att >= 30 and avg_marks >= 40:
        label = "At Risk"
    else:
        label = "Failing"

    return label

results = []
for s in students:
    label = classify_student(s)
    results.append({"name": s["name"], "attendance": s["attendance"],
                    "average_marks": sum(s["marks"])//len(s["marks"]),
                    "label": label})
for r in results:
    print(f"{r['name']}: Attendance={r['attendance']}%, Avg Marks={r['average_marks']} → {r['label']}")


