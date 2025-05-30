class CustomReward(Wrapper):
    def __init__(self, env=None):
        super(CustomReward, self).__init__(env)
        # Actualizamos el espacio de observación y el espacio de acción.
        #self.observation_space = Box(low=0, high=255, shape=(HEIGHT, WIDTH), dtype=np.float32)
        self.action_space = Discrete(env.action_space.n)
        
        # Inicializamos la información adicional.
        self.info = {}
        
        # Inicializamos la posición x y las variables necesarias.
        self.current_x = 40
        #self.last_coins = 0  # Para contar las monedas recogidas

    def step(self, action):
        # Ejecutamos la acción en el entorno y obtenemos el nuevo estado, la recompensa, si ha terminado el episodio y la información adicional.
        obs, reward, done, trunk, info = self.env.step(action)
        self.info = info
        
        # Procesamos la imagen (por ejemplo, convertirla a escala de grises, redimensionarla, normalizarla).
        obs = process_frame(obs)
        
        # Calculamos las monedas recogidas.
        # coins_collected = info.get('coins', 0)
        # coins_reward = coins_collected - self.last_coins  # Diferencia de monedas recogidas
        
        # Actualizamos la recompensa en función de las monedas recogidas
        # reward += coins_reward * 0.5  # Bono de recompensa por cada moneda recogida

        # Actualizamos la posición x de Mario.
        x_pos = info.get("x_pos", self.current_x)
        progress_reward = (x_pos - self.current_x) * 0.1
        reward += progress_reward
        self.current_x = x_pos

        # Actualizamos las monedas recogidas en el último paso.
        # self.last_coins = coins_collected
        
        # Recompensa terminal positiva si Mario llega a la bandera
        if info.get('flag_get', False):  # Si Mario ha alcanzado la bandera
            reward += 50  # Recompensa positiva por alcanzar la meta
        
        # Recompensa terminal negativa si el episodio termina y Mario no llega a la meta
        if done and not info.get('flag_get', False):  # Si no ha alcanzado la bandera
            reward -= 20  # Recompensa negativa por no llegar a la meta

        # Modificamos la recompensa para que sea más manejable
        reward = reward / 10.  # Escalamos la recompensa

        return obs, reward, done, trunk, info

    def reset(self, **kwargs):
        # Reiniciamos las variables necesarias
        self.current_x = 40
        # self.last_coins = 0  # Reiniciamos el contador de monedas
        
        # Reiniciamos el entorno y obtenemos el estado inicial procesado
        obs, info = self.env.reset()
        obs = process_frame(obs)  # Procesamos la imagen
        return obs, info
