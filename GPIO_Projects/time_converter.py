x=333

hours=int(x/3600)
minutes=int((x/3600-hours)*60)
seconds=x-hours*3600-minutes*60
print("x seconds is- %02d:%02d:%02d" %(hours, minutes, seconds))
