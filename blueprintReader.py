from pynbt import NBTFile

with open('5x4x2.bpt', 'rb') as file:
    nbt = NBTFile(file)
    print(nbt.pretty())

