# Jupyter Notebook for Django

This project serves as a template for integrating Jupyter Notebook 
for any Django project. The necessary packages are specifically 
`ipython==8.14.0`, `jupyter==1.0.0` and `notebook==5.7.5`. After
creating the Python virtual environemnt `venv` and installing the 
packages, run Jupyter Notebook with the simple command
```
jupyter notebook
```

This project has a "course" application to demonstrate 
object-oriented programming for Django models. There are 5 models
in this application, namely `Course`, `InPersonCourse`, 
`OnlineCourse`, `Exam` and `Student`. The requirements are as follows:
- An instance of Student can register many courses.
- An instance of Course can be either in-person or online
- There can be many exams registered for a course, and each exam has
  a grade and is associated with a student. 

There can be an alternative way to program the `Exam` model in order
to associate it better with the models `Student`. That is to create
a model `Score` like the following
```python
class Score(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="score",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="score",
    )
    grade = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.exam.id} - {self.student.id} : {self.grade}"
```

With this added model, a `Student` instance can access the score in the
following way
```python
scores = student.score.all()
```

We write the models depending on what we need. This project is only to
how to access Django models using Jupyter Notebook.