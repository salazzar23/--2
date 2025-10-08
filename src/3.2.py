def format_record(rec: tuple[str, str, float]) -> str:
    fio, group, gpa = rec

    if not fio.strip() or not group.strip() or not isinstance(gpa, (int, float)):
        raise ValueError("Некорректная запись")

    fio_parts = fio.strip().split()
    if len(fio_parts) < 2:
        raise ValueError("Неверное ФИО")

    surname = fio_parts[0].capitalize()
    initials = ''.join(p[0].upper() + '.' for p in fio_parts[1:])
    return f"{surname} {initials}, гр. {group.strip()}, GPA {gpa:.2f}"
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))