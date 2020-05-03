<template>
  <div class="register-container">
    <div class="register">
      <el-input v-model="username" placeholder="请输入用户名"/>
      <el-input v-model="password" placeholder="请输入密码" show-password/>
      <el-button id="reg_button" type="primary" @click="reg()">立即注册</el-button>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {base_url} from "../assets/js/base";

  export default {
    name: 'Register',
    data () {
      return {
        username: '',
        password: '',
        reg_url: base_url + 'user/reg',
      }
    },
    methods: {
      //注册
      reg() {
        if (this.username == '' || this.password == '') {
          this.errorMsg("必填字段不能为空")
          return
        }
        var data = {username: this.username, password: this.password}
        axios.post(this.reg_url, data, {headers: {'Content-Type': 'application/json'}})
        .then(response => {
          if (response.data.code != 0) {
            this.errorMsg(response.data.msg);
          } else {
            this.successMsg("注册成功");
            this.$router.push({ path: '/login' })
          }
        })
        .catch(error => {
          this.errorMsg(error);
        })
      },
      successMsg(msg) {
        this.$message({
          showClose: true,
          message: msg,
          type: 'success',
          duration: 2000
        });
      },
      errorMsg(msg) {
        this.$message({
          showClose: true,
          message: msg,
          type: 'error',
          duration: 2000
        });
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background: url("../assets/images/background.jpeg") no-repeat center center;
    background-size: cover;
  }
  .register {
    width: 300px;
  }
  #reg_button {
    width: 300px;
    margin-top: 10px;
  }
</style>
