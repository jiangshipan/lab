<template>
        <div class="add_email">
        <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="实验" v-if="this.$route.query.identity_type != '管理员'">
            <el-select v-model="form.eid" placeholder="请选择实验">
                <el-option v-for="(item, index) in labs" :key="index" :label="item.name" :value="item.id"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="公告内容">
            <el-input type="textarea" v-model="form.content"></el-input>
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
  name: 'AddEmail',
  data () {
    return {
        form: {
            content: '',
            eid: '',
        },
        labs: [],
        add_email_url: base_url + 'email/add',
        get_all_exp_url: base_url + 'experiment/get_pass'     
    }
  },
  mounted() {
      this.get_all_exp()
  },
  methods: {
      submit_form() {  
        axios.get(this.add_email_url + '?eid=' + this.form.eid + "&content=" + this.form.content)
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
      get_all_exp() {
        axios.get(this.get_all_exp_url)
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
        this.form.content = ''
        this.form.eid = ''
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
  .add_email {
    margin: 10em auto;
    width: 600px;
  }
  .ipt-container {
    display: flex;
    align-items: center;
  }
</style>
 