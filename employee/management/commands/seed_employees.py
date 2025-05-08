import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from employee.models import Employee
from department.models import Department
from attendance.models import Attendance
from performance.models import Performance


class Command(BaseCommand):
    help = 'Seeds the database with fake employee data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # 清除现有数据（可选）
        self.stdout.write('Deleting old data...')
        Performance.objects.all().delete()
        Attendance.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()

        # 创建部门
        self.stdout.write('Creating departments...')
        departments = [
            Department.objects.create(department_name='Engineering'),
            Department.objects.create(department_name='Marketing'),
            Department.objects.create(department_name='Finance'),
            Department.objects.create(department_name='Human Resources'),
            Department.objects.create(department_name='Sales'),
            Department.objects.create(department_name='Research & Development'),
            Department.objects.create(department_name='Customer Support'),
        ]

        # 创建员工和相关数据
        self.stdout.write('Creating employees, attendance and performance records...')

        with transaction.atomic():
            for i in range(50):
                # 创建员工
                employee = Employee.objects.create(
                    name=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    address=fake.address(),
                    join_date=fake.date_between(start_date='-5y', end_date='today'),
                    department=random.choice(departments)
                )

                # 为每个员工创建考勤记录（过去30天）
                today = datetime.now().date()
                for day_offset in range(30):
                    date = today - timedelta(days=day_offset)
                    # 跳过周末
                    if date.weekday() < 5:  # 0-4表示周一到周五
                        Attendance.objects.create(
                            employee=employee,
                            date=date,
                            status=random.choice(['present', 'absent', 'late']),
                        )

                # 为每个员工创建2-4条绩效评估记录（确保日期不重复）
                # 生成员工入职日期到今天之间的所有可能日期
                join_date = employee.join_date
                possible_dates = []
                current_date = join_date
                while current_date <= today:
                    possible_dates.append(current_date)
                    current_date += timedelta(days=1)

                # 如果可能的日期少于要创建的评估记录数量，则调整评估记录数量
                num_reviews = min(random.randint(2, 4), len(possible_dates))

                # 随机选择不重复的日期
                if possible_dates:
                    review_dates = random.sample(possible_dates, num_reviews)

                    for review_date in review_dates:
                        Performance.objects.create(
                            employee=employee,
                            review_date=review_date,
                            rating=str(random.randint(1, 5))  # 转为字符串以匹配您的模型
                        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created 50 employees with related data!'))