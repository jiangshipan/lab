<template>
        <div class="add_lab">
        <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="实验室">
            <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="资产">
            <el-input type="textarea" v-model="form.devices"></el-input>
        </el-form-item>
        <el-form-item label="公告内容">
            <el-input type="textarea" v-model="form.notice"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submit_form()">立即发送</el-button>
            <el-button @click="clean_all()">取消</el-button>
        </el-form-item>
        </el-form>
  </div>
</template>

<script>
import axios from 'axios'
import {base_url} from "../assets/js/base";

export default {
  name: 'AddLab',
  data () {
    return {
        form: {
            name: '',
            notice: '',
            devices: ''
        }, 
        add_url: base_url + 'laboratory/add_new'
    }
  },
  mounted() {
      this.get_laboratories()
  },
  methods: {
      submit_form() {  
        var data = {name: this.form.name, notice: this.form.notice, devices: this.form.devices}
        axios.post(this.add_url, data, {headers: {'Content-Type': 'application/json'}})        
        .then(response => {
          if (response.data.code != 0) {
            this.errorMsg(response.data.msg);
          } else {
            this.successMsg("发送成功");
            this.clean_all();
          }
        })
        .catch(error => {
          this.errorMsg(error);
        })
      },
      clean_all() {
        this.form.name = ''
        this.form.notice = ''
        this.form.devices = ''

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

<style scoped>
  .add_lab {
    margin: 10em auto;
    width: 600px;
  }
  .ipt-container {
    display: flex;
    align-items: center;
  }
</style>