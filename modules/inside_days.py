import datetime


class WeekTimeInterval:
    def __init__(self, day_start, hour_start, day_end, hour_end):
        self.day_start = day_start
        self.day_end = day_end
        self.hour_start = hour_start
        self.hour_end = hour_end

    def day_shift_time_tuple(self, delta_days, time):
        """create a datetime tuple of shifted day- days and clock"""
        clock_format = '%H:%M:%S'
        clock = datetime.datetime.strptime(time, clock_format)

        shifted_datetime = datetime.datetime.combine(
            datetime.datetime.now().date() + datetime.timedelta(days=delta_days), clock.time())
        return shifted_datetime

    def shift_from_toady_time_tuple(self, day, hour):
        shifted_datetime = self.day_shift_time_tuple(day - self.iso2h_day_convert(datetime.datetime.now().isoweekday()),
                                                     hour)
        return shifted_datetime

    def iso2h_day_convert(self, iso_day):
        if 1 <= iso_day <= 6:
            day = iso_day + 1
        elif iso_day == 7:
            day = 1
        else:
            day = None
        return day

    def h2iso_convert_day(self, ay):
        if 2 <= day <= 7:
            iso_day = day - 1
        elif day == 1:
            iso_day = 7
        return iso_day

    def get_datetimes(self):
        start_datetime = self.shift_from_toady_time_tuple(self.day_start, self.hour_start)
        if self.day_end - self.day_start >= 0:
            end_datetime = self.shift_from_toady_time_tuple(self.day_end, self.hour_end)
        else:
            end_datetime = self.shift_from_toady_time_tuple(self.day_end + 7, self.hour_end)

        if start_datetime > end_datetime:
            end_datetime += datetime.timedelta(days=7)
        return start_datetime, end_datetime


if __name__ == "__main__":
    a = WeekTimeInterval(5, "14:00:00", 4, "12:00:00").get_datetimes()
    print(a)
