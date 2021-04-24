<template>
    <div class="race">
        <div class="joystick" ref="joystickBox">
            <div class="joystick-moveable"  ref="joystick"></div>
            <div>{{fps}}</div>
        </div>
        <img id="image" ref="image"/>
    </div>
</template>

<script lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { socket } from '@/main'
import lodash from 'lodash'

export default {
    setup() {
        const joystick = ref<HTMLElement | null>(null)
        const joystickBox = ref<HTMLElement | null>(null)
        const image = ref<HTMLImageElement | null>(null)
        const offset = ref<DOMRect | null>(null)
        const joystickRadius = ref(60)
        const _fps = ref(0)
        const fps = ref(0)

        setInterval(() => {
            fps.value = _fps.value
            _fps.value = 0
        }, 1000)
        
        const send = lodash.throttle((speed: any, direction: any) => {
            socket.emit('drive', Int8Array.of(speed, direction))
        }, 100)

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

                const speed = Math.round(Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2)) / joystickRadius.value * (y > 0 ? -100 : 100))
                const direction = Math.round(x / 80 * 100)

                send(speed, direction)
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
            socket.emit('drive', Int8Array.of(0, 0))
        }

        function touchmove(event: TouchEvent) {
            const touch = event.touches[0]
            updateButton(touch)
            
            
        }

        socket.on('image', (data: any) => {
            // console.log(typeof data)
            _fps.value += 1
            if (image.value != null)
                image.value.src = "data:image/jpeg;base64," + data
        })

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

        return {joystick, joystickBox, joystickRadius, image, fps}
    }
}
</script>

<style lang="scss" scoped>
.race {
    width: 100%;
    height: 100%;
    position: relative;

    #image {
        width: 100%;
        height: 100%;
    }

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