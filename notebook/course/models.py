from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    season = models.CharField(max_length=7, blank=True, null=True, default="")
    year = models.PositiveIntegerField(blank=True, null=True)
    created_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title

    @property
    def students(self):
        return self.student_set.all()

    @property
    def is_in_person(self):
        return self.in_person_course.all().count() > 0

    @property
    def is_online(self):
        return self.online_course.all().count() > 0

    @property
    def course_location(self):
        if self.is_in_person:
            return self.in_person_course.all().first().class_room_location
        return ""

    @course_location.setter
    def course_location(self, location=""):
        if self.is_in_person:
            in_person_course = self.in_person_course.all().first()
            in_person_course.class_room_location = location
            in_person_course.save()
        else:
            self.in_person_course.model.objects.create(
                course=self,
                class_room_location=location,
            )
        return location

    @property
    def course_url(self):
        if self.is_online:
            return self.online_course.all().first().course_url
        return ""

    @course_url.setter
    def course_url(self, url=""):
        if self.is_online:
            online_course = self.online_course.all().first()
            online_course.course_url = url
            online_course.save()
        else:
            self.online_course.model.objects.create(
                course=self,
                course_url=url,
            )
        return url

    @property
    def get_exams(self):
        return self.exam.all()

    def add_exam(self, grade):
        exam, _ = self.exam.model.objects.get_or_create(
            course=self,
            grade=grade,
        )
        return exam

    @property
    def semester(self):
        return f"{self.season} {self.year}"


class InPersonCourse(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="in_person_course",
    )
    class_room_location = models.CharField(
        max_length=128, blank=True, null=True, default=""
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.course} at {self.class_room_location}"


class OnlineCourse(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="online_course",
    )
    course_url = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default="",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.course} at {self.course_url}"


class Exam(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="exam",
    )
    grade = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.course.title}: {self.grade}"

    @property
    def students(self):
        return self.student_set.all()


class Student(models.Model):
    first_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default="",
    )
    last_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default="",
    )
    student_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default="",
    )
    courses = models.ManyToManyField(Course)
    exams = models.ManyToManyField(Exam)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def get_courses(self):
        return self.courses.all()

    @property
    def get_exams(self):
        return self.exams.all()

    def add_course(self, course=Course):
        self.courses.add(course)
        return course.title

    def add_exam(self, exam=Exam):
        self.exams.add(exam)
        return f"{exam.course.title}: {exam.grade}"

    def filter_exams(self, title="", grades: list = []):
        if len(grades) > 2:
            raise ValueError("grades list has a maximum length of 2")
        if title == "":
            if len(grades) == 1:
                return self.exams.filter(grade=grades[0])
            else:
                return self.exams.filter(
                    grade__gte=grades[0],
                    grade__lte=grades[1],
                )
        else:
            if len(grades) == 1:
                return self.exams.filter(
                    course__title=title,
                    grade=grades[0],
                )
            else:
                return self.exams.filter(
                    course__title=title,
                    grade__gte=grades[0],
                    grade__lte=grades[1],
                )
