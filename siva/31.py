
projects = []

def add_project(data):
    if not isinstance(data, dict) or "id" not in data or "task" not in data:
        return {"error": "Malformed payload. Expected dict with 'id' and 'task'."}
    projects.append(data)
    return {"message": "Project added successfully", "project": data}

def list_projects():
    return {"items": projects}

def search_projects(query):
    results = []
    for pro in projects:
        if query.lower() in str(pro.get("id", "")).lower() or query.lower() in pro.get("task", "").lower():
            results.append(pro)
    return {"results": results}

def router(request, data=None):
    try:
        parts = request.strip().split()
        if len(parts) != 2:
            return {"error": "Malformed request. Expected 'METHOD /path'."}
        method, path = parts

        if method == "GET" and path == "/items":
            return list_projects()
        elif method == "POST" and path == "/items":
            return add_project(data)
        elif method == "GET" and path == "/search":
            if not data or "query" not in data:
                return {"error": "Search requires a 'query' field."}
            return search_projects(data["query"])
        else:
            return {"error": f"Unknown path or method: {method} {path}"}
    except Exception as e:
        return {"error": f"Internal failure: {e}"}

# --- Demo Run ---
if __name__ == "__main__":
    # Add employees
    print(router("POST /items", {"id": 101, "task": "project K"}))
    print(router("POST /items", {"id": 102, "task": "project S"}))

    # List employees
    print(router("GET /items"))

    # Search employees
    print(router("GET /search", {"query": "pro"}))

    # Invalid request
    print(router("DELETE /items"))