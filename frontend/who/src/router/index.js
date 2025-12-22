import { createRouter, createWebHistory } from "vue-router";

import Who from "@/views/desktop/Who.vue"
import HostConfig from "@/views/desktop/Host.vue"
import RoomConfig from  "@/views/desktop/Room.vue"
import HostGame from "@/views/desktop/Game.vue"

import Join from "@/views/mobile/Join.vue"
import PoolSelect from "@/views/mobile/Pool.vue"
import PlayerGame from "@/views/mobile/Game.vue"

const routes = [
  { path: "/", redirect: "/who" },
  { path: "/who", component: Who },
  { path: "/who/host", component: HostConfig },
  { path: "/who/host/room", component: RoomConfig },
  { path: "/who/host/game", component: HostGame },
  { path: "/who/join", component: Join },
  { path: "/who/player/pool", component: PoolSelect },
  { path: "/who/player/game", component: PlayerGame },
];

export default createRouter({
  history: createWebHistory(),
  routes
});
