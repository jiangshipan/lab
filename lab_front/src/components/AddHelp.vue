<template>
        <div class="add_help">
        <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="实验室">
            <el-select v-model="form.lab_no" placeholder="请选择实验室">
                <el-option v-for="(item, index) in labs" :key="index" :label="item.name" :value="item.id"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="问题描述">
            <el-input type="textarea" v-model="form.question"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submit_form()">立即创建</el-button>
            <el-button @click="clean_all()">取消</el-button>
        </el-form-item>
        </el-form>
  </div>
</template>

<script>
import axios from 'axios'
import {base_url} from "../assets/js/base";

export default {
  name: 'AddHelp',
  data () {
    return {
        form: {
            question: '',
            lab_no: '',
        },
        labs: [],
        add_help_url: base_url + 'laboratory/add_help',
        get_all_labs_url: base_url + 'laboratory/getAll'     
    }
  },
  mounted() {
      this.get_laboratories()
  },
  methods: {
      submit_form() {  
        axios.get(this.add_help_url + "?lab_id=" + this.form.lab_no + "&question=" + this.form.question)
        .then(response => {
          if (response.data.code != 0) {
            this.errorMsg(response.data.msg);
          } else {
            this.successMsg("反馈成功");
            this.clean_all();
          }
        })
        .catch(error => {
          this.errorMsg(error);
        })
      },
      get_laboratories() {
        axios.get(this.get_all_labs_url)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.labs = res.data
            console.log(this.labs)
        })
        .catch(error => {
          this.errorMsg('网络错误, 暂时不能访问')
        })
      },
      clean_all() {
        this.form.question = ''
        this.form.lab_no = ''
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
  .add_help {
    margin: 10em auto;
    width: 600px;
  }
  .ipt-container {
    display: flex;
    align-items: center;
  }
</style>
 