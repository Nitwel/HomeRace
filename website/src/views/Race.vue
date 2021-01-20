<template>
    <div class="race">
        <div class="joystick" ref="joystickBox">
            <div class="joystick-moveable"  ref="joystick"></div>
        </div>
    </div>
</template>

<script lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

export default {
    setup() {
        const joystick = ref<HTMLElement | null>(null)
        const joystickBox = ref<HTMLElement | null>(null)
        const offset = ref<DOMRect | null>(null)
        const joystickRadius = ref(60)

        function updateButton(touch: Touch) {
            if(offset.value != null && joystick.value != null) {

                let x = touch.pageX - offset.value.left - offset.value.width / 2
                let y = touch.pageY - offset.value.top - offset.value.height / 2
                const d = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2))

                if( d > joystickRadius.value) {
                    const angle = Math.atan2(y, x)
                    x = Math.cos(angle) * joystickRadius.value
                    y = Math.sin(angle) * joystickRadius.value
                }
                joystick.value.style.transform = `translate(${x - offset.value.width / 2}px, ${y - offset.value.height / 2}px)`
            }
        }

        function touchstart(event: TouchEvent) {
            const touch = event.touches[0]
            updateButton(touch)
        }

        function touchend(event: TouchEvent) {
            if(offset.value != null && joystick.value != null) {
                const x = -offset.value.width / 2
                const y = -offset.value.height / 2
                joystick.value.style.transform = `translate(${ x }px, ${ y }px)`
            }
        }

        function touchmove(event: TouchEvent) {
            const touch = event.touches[0]
            updateButton(touch)
            
            
        }

        onMounted(() => {
            if(joystick.value != null && joystickBox.value != null) {
                joystickBox.value.style.width = joystickRadius.value * 2 + 'px'
                joystickBox.value.style.height = joystickRadius.value * 2 + 'px'
                offset.value = joystick.value.getBoundingClientRect()
            }
        })

        document.addEventListener('touchstart', touchstart)
        document.addEventListener('touchend', touchend)
        document.addEventListener('touchmove', touchmove)
        
        onBeforeUnmount(() => {
            document.removeEventListener('touchstart', touchstart)
            document.removeEventListener('touchend', touchend)
            document.removeEventListener('touchmove', touchmove)
        })

        return {joystick, joystickBox, joystickRadius}
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
        bottom: 30px;
        left: 30px;
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