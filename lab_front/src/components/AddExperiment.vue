<template>
        <div class="add_experiment">
            <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="实验名称">
            <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="活动时间">
            <el-col :span="12">
            <el-input placeholder="输入开始时间" v-model="form.start_time" style="width: 100%;"></el-input>
            </el-col>
            <el-col :span="12">
            <el-input type="text" placeholder="输入结束时间" v-model="form.end_time" style="width: 100%;"></el-input>
            </el-col>
        </el-form-item>
        <el-form-item label="实验说明">
            <el-input type="textarea" v-model="form.remark"></el-input>
        </el-form-item>
        <el-form-item label="实验室">
            <el-select v-model="form.lab_no" placeholder="请选择实验室">
                <el-option v-for="(item, index) in labs" :key="index" :label="item.name" :value="item.id"></el-option>
            </el-select>
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
  name: 'AddExperiment',
  data () {
    return {
        form: {
            name: '',
            start_time: '',
            end_time: '',
            remark: '',
            lab_no: '',
        },
        labs: [],
        add_experiment_url: base_url + 'experiment/add',
        get_all_labs_url: base_url + 'laboratory/getAll'     
    }
  },
  mounted() {
      this.get_laboratories()
  },
  methods: {
      submit_form() {  
        var data = {name: this.form.name, start_time: this.form.start_time, end_time: this.form.end_time, 
        remark: this.form.remark, lab_no: this.form.lab_no}
        axios.post(this.add_experiment_url, data, {headers: {'Content-Type': 'application/json'}})
        .then(response => {
          if (response.data.code != 0) {
            this.errorMsg(response.data.msg);
          } else {
            this.successMsg("申请成功");
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
        this.form.name = ''
        this.form.start_time = ''
        this.form.end_time = ''
        this.form.remark = ''
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
  .add_experiment {
    margin: 10em auto;
    width: 600px;
  }
  .ipt-container {
    display: flex;
    align-items: center;
  }
</style>
 