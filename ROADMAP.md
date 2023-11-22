### Step 1 : Taking Input

- we NEED to basic UI (need to discuss) 

- course duration and status
- Syllabus/Courses
- GPA # have to discuss if we need it
- Technologies and tools they know
- Technologies and tools they are interested in
- Projects they have worked on (GitHub Link) 
- Output Oriented interests  .... aarti 

### Step 2 : Processing Input

```python
input_data = {
    "course_duration": [6, 2],
    "syllabus": ["Data Analysis", "Web Development", "Machine Learning"],
    "cgpa": [7.5, 8.0],
    "technologies_known": ["Python", "HTML5", "Javascript"],
    "technologies_interested": ["Machine Learning", "Web Development"],
    "projects": ["Github.com/user123/projectA", "Github.com/user123/projectA"]
}
```

- ispe pre processing karna h

### Step 3 : Recommend Technologies and Courses

- recommend basic tech they need to learn .... 

- we probably have to use scikit-learn 

- Train a decision tree model 

  - offline data base of courses => choose courses
  - scrape related courses in RT from sites 

### Step 4 : Project recommendations

- Based on the student's technologies known and projects they've worked on

- cater 3 cat (thanks to aarti) 

       - beginner : simple project ideas, eg calc,etc
       - intermediate : upr k + some basic existing projs they can contribute to 
       - advanced : popular existing proj recommendations

- recommend from a predefined data base - simple

- freelancing sites 

### Step 5: LinkedIn Job Profile Recommendations    

- based on skills and interests 
- use beautifulsoup4 to scrap relevant job from linkedin search results 

https://www.linkedin.com/jobs/search/?currentJobId=3623351494&keywords=data%20analyst&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true

- query strings can be used

### Step 6: Output 

- ranking
- 
