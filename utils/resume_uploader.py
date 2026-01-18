def process_resumes(files):
    resumes = []
    for f in files:
        resumes.append({
            "name": f.name,
            "content": f.read().decode('latin-1')
        })
    return resumes
