<template>
    <div class="race">
        <div class="joystick" @mouseenter="mouseenter" @mouseleave="mouseleave">
            <div class="joystick-moveable"></div>
        </div>
    </div>
</template>

<script lang="ts">
import { onBeforeUnmount } from 'vue'

export default {
    setup() {

        function mouseenter() {
            console.log("enter")
        }

        function mouseleave() {
            console.log("leave")
        }

        function mousedown() {
            console.log("down")
        }

        function mouseup() {
            console.log("up")
        }

        function mousemove() {
            console.log("move")
        }

        document.addEventListener('touchstart', mousedown)
        document.addEventListener('touchend', mouseup)
        document.addEventListener('touchmove', mousemove)
        
        onBeforeUnmount(() => {
            document.removeEventListener('touchstart', mousedown)
            document.removeEventListener('touchend', mouseup)
            document.removeEventListener('touchmove', mousemove)
        })

        return {mouseenter, mouseleave}
    }
}
</script>

<style lang="scss" scoped>
.race {
    width: 100%;
    height: 100%;
    position: relative;

    .joystick {
        position: absolute;
        bottom: 60px;
        left: 60px;
        width: 200px;
        height: 200px;
        background-color: var(--gray);
        border-radius: 50%;

        &-moveable {
            background-color: red;
            width: 50px;
            height: 50px;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border-radius: 50%;
        }
    }
}
</style>