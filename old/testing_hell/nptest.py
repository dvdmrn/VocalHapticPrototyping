import numpy as np
from scipy.interpolate import interp1d


# a = np.array([(1,'hi'),(2,'mommy')])

# print(a['hi'])

# x = np.array([[(1,2.,'Hello'), (2,3.,"World")],[(7,9.,'Hi'), (2,3.,"Mommy")]],
              # dtype=[('foo', 'f4'),('bar', 'f4'), ('baz', 'S10')])

# data = np.zeros(4, dtype={'names':('name', 'age', 'weight'),
#                           'formats':('U10', 'i4', 'f8')})


# data[0]["name"] = "mommy"
# data[0]["age"] = 69
# data[0]["weight"] = 420.69

# data[1]["name"] = "fred"
# data[1]["age"] = 5
# data[1]["weight"] = 1337

# keys = dtype=[('time', 'f2'),('f0_Hz', 'f4'), ('frame', 'u4'), ('rms', 'u4')]
# x = np.array([(0.55,1.2,432,555),(1337.,0.699999,420,69)], keys)
# print(x['time'])

# x = np.zeros(100, keys)
# x[4]["time"] = 4.3
# x[4]["f0_Hz"] = 7.8

# print(x[4])



xs = np.array((3.,4.,5.,6.,7.,8.,9.))
pitch_values = np.array((1.,1.,0.,2.,1.,0.,11.))

trans = np.array((xs,pitch_values))
print(trans.T)

sa = np.array(trans.T, dtype=[('x','f4'),('Hz','f4')])
# arr = np.core.records.fromarrays([pitch_values,xs],names="Hz,x")


print(sa)


# new = sa[sa["Hz"]!=0]
# print(new["x"])


interp = interp1d([0,2,4,6],[80,100,90,100], kind="cubic")

print(interp)
a=np.array([('Rex', 9, 81.0), ('Fido', 3, 27.0)],
              dtype=[('name', 'U10'), ('age', 'i4'), ('weight', 'f4')])
new = a[a["age"]!=3]
print(new)
# pitch_x = np.array([1.,2.,3.,4.,5.,6.,7.])

# for i in range(0,5):
# 	print("hwllo",4-i)
# 	if pitch_values[4-i] == 0:
# 		d

# print(pitch_values)
# x = np.interp([1,2,3,4,5],[0,3,4,6],[1,8,np.nan,2])
# print(x)