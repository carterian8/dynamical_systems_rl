from gym.envs.registration import register

register(
    id='dsys-v0',
    entry_point='gym_dsys.envs:LotkaVolterraEnv',
)
