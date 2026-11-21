class SimulationController:
    """Controla la ejecución de una simulación desde el frontend."""

    SPEEDS = (0.5, 1, 2, 4, 8)

    def __init__(self, simulation=None, ticks_per_second=1):
        self.simulation = simulation

        self.ticks_per_second = ticks_per_second
        self.speed_index = 1

        self.paused = True
        self.accumulated_time = 0.0

    @property
    def speed(self):
        return self.SPEEDS[self.speed_index]

    @property
    def tick(self):
        if self.simulation is None:
            return 0

        return self.simulation.tick

    @property
    def finished(self):
        """Indica si la simulación ha terminado."""

        return (
            self.simulation is None
            or self.simulation.is_finished
        )

    def set_simulation(self, simulation):
        """Asigna una simulación al controlador."""

        self.simulation = simulation
        self.accumulated_time = 0.0
        self.paused = True

    def play(self):
        """Reanuda la simulación si todavía quedan criaturas."""

        if self.finished:
            self.pause()
            return

        self.paused = False

    def pause(self):
        """Pausa la simulación."""

        self.paused = True
        self.accumulated_time = 0.0

    def toggle_pause(self):
        """Alterna entre pausa y ejecución."""

        if self.paused:
            self.play()
        else:
            self.pause()

    def set_speed(self, speed):
        """Establece una velocidad admitida."""

        if speed not in self.SPEEDS:
            raise ValueError(
                f"Velocidad no válida: {speed}. "
                f"Velocidades permitidas: {self.SPEEDS}"
            )

        self.speed_index = self.SPEEDS.index(speed)

    def increase_speed(self):
        """Aumenta la velocidad un nivel."""

        if self.speed_index < len(self.SPEEDS) - 1:
            self.speed_index += 1

    def decrease_speed(self):
        """Reduce la velocidad un nivel."""

        if self.speed_index > 0:
            self.speed_index -= 1

    def step(self):
        """Ejecuta exactamente un tick manual."""

        if self.finished:
            self.pause()
            return

        self.simulation.run_tick()
        self.accumulated_time = 0.0

        if self.finished:
            self.pause()

    def update(self, delta_time):
        """Actualiza la simulación según el tiempo transcurrido."""

        if self.paused or self.simulation is None:
            return

        if self.finished:
            self.pause()
            return

        if self.ticks_per_second <= 0:
            return

        tick_interval = (
            1.0 / (self.ticks_per_second * self.speed)
        )

        self.accumulated_time += delta_time

        while self.accumulated_time >= tick_interval:
            self.simulation.run_tick()
            self.accumulated_time -= tick_interval

            if self.finished:
                self.pause()
                break
