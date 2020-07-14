import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR


class TrevBot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylon()
        await self.build_assimilators()
        await self.expand()

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylon(self):
        if self.supply_left < 6 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexuses[0])

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            vespenes = self.state.vespene_geyser.closer_than(10.0, nexus)
            for v in vespenes:
                if self.can_afford(ASSIMILATOR):
                    if not self.units(ASSIMILATOR).closer_than(1, v).exists:
                        worker = self.select_build_worker(v.position)
                        if worker is not None:
                            await self.do(worker.build(ASSIMILATOR, v))

    async def expand(self):
        if self.units(NEXUS).amount < 3:
            if self.can_afford(NEXUS):
                await self.expand_now()


run_game(
    maps.get("AbyssalReefLE"),
    [
        Bot(Race.Protoss, TrevBot()),
        Computer(Race.Terran, Difficulty.Easy),
    ],
    realtime=False)
