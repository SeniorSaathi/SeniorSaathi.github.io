import csv
import datetime
import os
import bs4
import requests
import pandas as pd
from github_repo_score import *

class Student:
    def __init__(self, name, course_name, current_sem, duration, cgpa, field_of_interest=[], projects=[]):
        self.name = name
        self.course_name = course_name
        self.current_sem = float(current_sem)
        self.duration = float(duration)
        self.cgpa = cgpa
        self.field_of_interest = field_of_interest
        self.projects = projects
        self.remaining_duration = self.duration*2 - self.current_sem

    def github_repo_score(self, projects):
        return github_repo_score(projects)
    
    def cgpa_score(self, cgpa):
        # student who has less remaining duration is expected to have higher cgpa
        cgpa_score = self.cgpa*self.remaining_duration
        # todo: improve algo
    


    def display(self):
        print(self.name)
        # print(self.course_name)
        # print(self.current_sem)
        # print(self.duration)
        # print(self.cgpa)
        # print(self.field_of_interest)
        # print(self.projects)
                
    
if __name__ == '__main__':
    student_data = os.path.join("student-data", "student-data.csv")
    with open(student_data, newline='') as student_data:
        reader = csv.reader(student_data)
        header = next(reader)
        for row in reader:
            student = Student(row[1], row[4], row[5], row[6], row[7], row[8].split(","), [row[9], row[10], row[11]])
            student.display()
            repo_stats = student.github_repo_score(student.projects)
              

