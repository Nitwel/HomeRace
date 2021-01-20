<template>
  <router-view/>
</template>

<style lang="scss">

* {
  box-sizing: border-box;
  --light-gray: #C7C7C7;
  --gray: #585858;
  --dark-gray: #1E1E1E;
  --white: #ffffff;
}

body {
  margin: 0;
  z-index: 1;
}

#app {
  background-color: var(--light-gray);
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
  z-index: 2;
}

body, #app {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
}
</style>
