<template>
  <div class="sign-in">
    <el-form ref="form" status-icon :model="form" :rules="rule" label-width="80px">
      <el-form-item label="用户名称" prop="usr">
        <el-input v-model="form.usr" placeholder="输入您的昵称">
          <i slot="prefix" class="fas fa-user icon"></i>
        </el-input>
      </el-form-item>
      <el-form-item label="输入密码" prop="pwd">
        <el-input type="password" v-model="form.pwd" placeholder="输入您的密码">
          <i slot="prefix" class="fas fa-lock icon"></i>
        </el-input>
      </el-form-item>
      <el-form-item class="btn">
        <el-button type="primary" @click="SignIn">登录</el-button>
        <!-- <el-button @click="$emit('change')">注册</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data(){
    var validate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        callback();
      }
    };
    var validateUsr = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入用户名'));
      } else {
        callback();
      }
    };
    return{
      form: {
        usr: '',
        pwd: ''
      },
      rule: {
        pwd: [{ validator: validate, trigger: 'blur' }],
        usr: [{ validator: validateUsr, trigger: 'blur' }]
      }
    }
  },
  methods: {
    SignIn: function(){
      if(this.form.usr=='caup'&&this.form.pwd=='sse'){
        this.$router.push('/tree/tree-record');
      }
      else{
        this.$message.error('用户名或密码错误！');
      }
      // let obj = this;
      // var params = new URLSearchParams();
      // params.append('usr', obj.form.usr); 
      // params.append('pwd', obj.form.pwd);

      // if(this.form.usr != '' && this.form.pwd != ''){
      //   axios({
      //     method: 'post',
      //     url: 'http://127.0.0.1:5000/signin',
      //     data: params,
      //     headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      //   })
      //   .then(function (response) {
      //     if(response.data.status == 'True'){
      //       obj.$root.$data.usr = obj.form.usr;
      //       obj.$root.$data.role = response.data.role;
      //       obj.$message({
      //         message: '成功登陆！',
      //         type: 'success'
      //       });
      //       obj.$router.push('/home');
      //     }
      //     else{
      //       obj.$message.error('用户名或密码错误！');
      //     }
      //   })
      //   .catch(function () {
      //     obj.$message.error('糟糕，哪里出了点问题！');
      //   });
      // }
      // else{
      //   this.$message.error('请确认输入内容全部正确！');
      // }
    }
  }
}
</script>

<style scoped>
.sign-in{
  float: right;
  margin-top: 180px;
  margin-right: 100px;
}
.btn{
  margin-top: 100px;
  margin-right: 10px;
}
</style>