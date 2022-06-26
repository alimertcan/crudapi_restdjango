# # from celery.loaders import periodic_task
# # from celery.task.schedules import crontab
# import celery
# from celery.schedules import crontab
#
#
#
#
# @periodic_task(run_every=(crontab(minute="*/1")))
# def randomly_increment_total_passengers():

a = [1, 2]
b = [1, 2]
print(a == b)
print(a is b)
# a= {[1,2]:"asd"}
b = {frozenset({1, 2, 3}): "asd"}

print(b.keys())


class myclass:
    lang = 'p'
    def say_hello():
        print("hello")
# print(a.keys())

myclass.__dict__['say_hello']()