import math

import pymem

m_iGlowIndex = 0x10488
dwGlowObjectManager = 0x5359988
dwEntityList = 0x4DFEF0C
dwLocalPlayer = 0xDE997C
dwClientState = 0x59F19C
dwClientState_ViewAngles = 0x4D90

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll


def calculateAngle(X, Y, Z, localPlayer):
    lpPosX = pm.read_float(localPlayer + 0x138 + (4 * 0))
    lpPosY = pm.read_float(localPlayer + 0x138 + (4 * 1))
    lpPosZ = pm.read_float(localPlayer + 0x138 + (4 * 2))

    deltaX = X - lpPosX
    deltaY = Y - lpPosY
    deltaZ = Z - lpPosZ

    ah = math.sqrt(deltaX*deltaX + deltaY*deltaY)
    yaw = math.atan2(-deltaZ, ah) * 180.0 / math.pi
    pitch = math.atan2(deltaY, deltaX) * 180 / math.pi

    return yaw, pitch

def fixAngles(x,y,z):
    if x > 89:
        x = 89
    if x < -89:
        x = -89
    while y > 180:
        y += 360
    while y < -180:
        y += 360

    if z != 0:
        z = 0

    return x, y, z


def getEntityPos(entity):
    X = pm.read_float(entity + 0x138 + (4 * 0))
    Y = pm.read_float(entity + 0x138 + (4 * 1))
    Z = pm.read_float(entity + 0x138 + (4 * 2))
    return X, Y, Z

def aimhack():
    while True:
        localPlayerInt = pm.read_int(client + dwLocalPlayer)
        ClientState = pm.read_int(engine + dwClientState)

        for i in range(0, 32):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)
            if entity and entity != localPlayerInt:
                entityHealth = pm.read_int(entity + 0x100)
                if entityHealth > 0:

                    entityPosX = getEntityPos(entity)[0]
                    entityPosY = getEntityPos(entity)[1]
                    entityPosZ = getEntityPos(entity)[2]

                    angle = calculateAngle(entityPosX,entityPosY, entityPosZ, localPlayerInt)

                    pm.write_float(dwClientState + dwClientState_ViewAngles, angle[0])
                    pm.write_float(dwClientState + dwClientState_ViewAngles + 4, angle[1])


def glowhack():
    while True:
        glow = pm.read_int(client + dwGlowObjectManager)
        for i in range(0, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                entityglowing = pm.read_int(entity + m_iGlowIndex)
                pm.write_float(glow + entityglowing * 0x38 + 0x8, float(1))  # red
                pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))  # green
                pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))  # blue
                pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)


if __name__ == '__main__':
    glowhack()
    # aimhack()
