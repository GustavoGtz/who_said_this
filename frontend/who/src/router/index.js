import { createRouter, createWebHistory } from "vue-router";

import Who from "@/views/Who.vue"

import Load from "@/views/desktop/Load.vue"
import RoomConfig from "@/views/desktop/RoomConfig.vue"
import HostConfig from  "@/views/desktop/HostConfig.vue"
import HostGame from "@/views/desktop/Game.vue"

import Client from "@/views/mobile/Client.vue"
import PoolSelection from "@/views/mobile/PoolSelection.vue"
import ClientGame from "@/views/mobile/Game.vue"

const routes = [
  { path: "/", redirect: "/who" },
  { path: "/who", component: Who},
  { path: "/who/host", component: Load },
  { path: "/who/host/room", component: RoomConfig },
  { path: "/who/host/config", component: HostConfig },
  { path: "/who/host/game", component: HostGame },
  { path: "/who/join", component: Client },
  { path: "/who/play/pool", component: PoolSelection },
  { path: "/who/play/game", component: ClientGame },
];

export default createRouter({
  history: createWebHistory(),
  routes
});
