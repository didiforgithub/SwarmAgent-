import swarmagent.environments.environment as env

curr_env = env.Environment("China","气候变化", auto_generate=True)
result = curr_env.run(3)
print(result)