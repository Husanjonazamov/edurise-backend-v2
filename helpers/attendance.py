from datetime import timedelta


def generate_attendance(course):
    create_at = course.create_at
    paired_days = []
    current_date = create_at
    end_date = create_at + timedelta(days=6 * 30)  # 6 oy

    while current_date <= end_date:
        if current_date.weekday() != 6:  # Yakshanbani o'tkazib yuborish
            if current_date.weekday() in [0, 2, 4]:  # Dushanba, Chorshanba, Juma
                paired_days.append(current_date)

        current_date += timedelta(days=1)

    return paired_days
