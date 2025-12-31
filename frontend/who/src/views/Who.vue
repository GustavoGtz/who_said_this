<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
    <div class="page-center">
        <div class="card">
            <div class="text-stack">
                <RouterLink to="who/host">Host Party</RouterLink>
                or
                <RouterLink to="who/join">Join Party</RouterLink>
            </div>
        </div>
    </div>
</template>
