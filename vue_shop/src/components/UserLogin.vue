<template>
  <div class="login-container">

    <!-- 背景装饰 -->
    <div class="background-grid"></div>

    <div class="background-glow glow-one"></div>
    <div class="background-glow glow-two"></div>
    <div class="background-glow glow-three"></div>

    <!-- 左侧品牌区域 -->
    <div class="brand-panel">

      <!-- Logo -->
      <div class="brand-header">
        <div class="brand-logo">
          <img src="../assets/mi-logo.png" alt="logo">
        </div>

        <div>
          <div class="brand-name">MI SHOP</div>
          <div class="brand-subtitle">ADMIN PLATFORM</div>
        </div>
      </div>

      <!-- 中间视觉 -->
      <div class="visual-area">

        <div class="orbit orbit-one"></div>
        <div class="orbit orbit-two"></div>
        <div class="orbit orbit-three"></div>

        <div class="core">

          <div class="core-inner">
            <span>MI</span>
          </div>

          <div class="core-ring"></div>

        </div>

        <!-- 浮动粒子 -->
        <span
          v-for="item in particles"
          :key="item.id"
          class="particle"
          :style="{
            left: item.left,
            top: item.top,
            animationDelay: item.delay
          }"
        ></span>

      </div>

      <!-- 左下角信息 -->
      <div class="brand-footer">
        <span>INTELLIGENT</span>
        <span>•</span>
        <span>FAST</span>
        <span>•</span>
        <span>SECURE</span>
      </div>

    </div>

    <!-- 右侧登录区域 -->
    <div class="login-panel">

      <div class="login-wrapper">

        <!-- 移动端 Logo -->
        <div class="mobile-logo">
          <img src="../assets/mi-logo.png" alt="logo">
          <span>MI SHOP</span>
        </div>

        <!-- 标题 -->
        <div class="login-header">

          <div class="welcome-label">
            WELCOME BACK
          </div>

          <h1>
            管理后台登录
          </h1>

          <p>
            登录您的管理控制中心
          </p>

        </div>

        <!-- 登录卡片 -->
        <div class="login-box">

          <!-- 顶部装饰线 -->
          <div class="top-line"></div>

          <el-form
            ref="formRef"
            :model="userform"
            :rules="urules"
            label-width="0px"
            class="form-style"
          >

            <!-- 用户名 -->
            <el-form-item prop="name">

              <div class="input-label">
                用户名
              </div>

              <el-input
                v-model="userform.name"
                placeholder="请输入用户名"
                size="large"
                class="tech-input"
              >

                <template #prefix>
                  <el-icon>
                    <User />
                  </el-icon>
                </template>

              </el-input>

            </el-form-item>

            <!-- 密码 -->
            <el-form-item prop="pwd">

              <div class="input-label">
                密码
              </div>

              <el-input
                v-model="userform.pwd"
                type="password"
                show-password
                placeholder="请输入密码"
                size="large"
                class="tech-input"
              >

                <template #prefix>
                  <el-icon>
                    <Lock />
                  </el-icon>
                </template>

              </el-input>

            </el-form-item>

            <!-- 按钮 -->
            <el-form-item>

              <div class="btns">

                <el-button
                  class="login-btn"
                  @click="login"
                >
                  <span>登录系统</span>
                  <span class="arrow">→</span>
                </el-button>

                <el-button
                  class="reset-btn"
                  @click="resetForm"
                >
                  重置
                </el-button>

              </div>

            </el-form-item>

          </el-form>

          <!-- 底部状态 -->
          <div class="system-status">

            <span class="status-dot"></span>

            <span>
              SYSTEM ONLINE
            </span>

          </div>

        </div>

        <!-- 底部版权 -->
        <div class="login-footer">
          <span>© 2026 MI SHOP ADMIN</span>
          <span>SECURE ACCESS</span>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'
import qs from 'qs'

const router = useRouter()

const formRef = ref()

const userform = ref({
  name: '',
  pwd: ''
})

const urules = {
  name: [
    {
      required: true,
      message: '请输入用户名',
      trigger: 'blur'
    }
  ],

  pwd: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    }
  ]
}

/**
 * 背景粒子
 */
const particles = Array.from(
  { length: 30 },
  (_, index) => ({
    id: index,
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
    delay: `${Math.random() * 5}s`
  })
)

/**
 * 重置
 */
const resetForm = () => {
  formRef.value.resetFields()
}

/**
 * 登录
 */
const login = () => {
  formRef.value.validate(async valid => {
    if (!valid) return

    try {
      const res = await axios.post(
        '/user/login',
        qs.stringify(userform.value)
      )

      if (res.data.status !== 200) {
        ElMessage.error(res.data.msg || '登录失败')
        return
      }

      ElMessage.success('登录成功')

      sessionStorage.setItem(
        'token',
        res.data.data.token
      )

      router.push('/home')
    } catch (error) {
      console.error('登录请求失败：', error)

      ElMessage.error(
        error.response?.data?.msg || '登录请求失败'
      )
    }
  })
}
</script>

<style lang="less" scoped>

* {
  box-sizing: border-box;
}

/* =========================
   页面
========================= */

.login-container {
  width: 100%;
  height: 100vh;
  min-height: 600px;

  display: grid;
  grid-template-columns: 1.05fr 0.95fr;

  position: relative;
  overflow: hidden;

  background:
    radial-gradient(
      circle at 15% 30%,
      rgba(59, 130, 246, 0.18),
      transparent 35%
    ),
    radial-gradient(
      circle at 80% 70%,
      rgba(139, 92, 246, 0.14),
      transparent 35%
    ),
    #050816;

  color: #ffffff;
}

/* =========================
   网格
========================= */

.background-grid {
  position: absolute;
  inset: 0;

  background-image:
    linear-gradient(
      rgba(255, 255, 255, 0.035) 1px,
      transparent 1px
    ),
    linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.035) 1px,
      transparent 1px
    );

  background-size: 40px 40px;

  mask-image: linear-gradient(
    to bottom,
    transparent,
    black 20%,
    black 80%,
    transparent
  );

  pointer-events: none;
}

/* =========================
   光晕
========================= */

.background-glow {
  position: absolute;

  border-radius: 50%;

  filter: blur(100px);

  pointer-events: none;
}

.glow-one {
  width: 350px;
  height: 350px;

  left: -100px;
  top: 10%;

  background: rgba(37, 99, 235, 0.18);
}

.glow-two {
  width: 300px;
  height: 300px;

  right: 10%;
  bottom: 0;

  background: rgba(124, 58, 237, 0.16);
}

.glow-three {
  width: 200px;
  height: 200px;

  right: 40%;
  top: 15%;

  background: rgba(14, 165, 233, 0.1);
}

/* =========================
   左侧
========================= */

.brand-panel {
  position: relative;

  padding: 48px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  border-right: 1px solid rgba(255, 255, 255, 0.08);

  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.045),
      rgba(255, 255, 255, 0.01)
    );

  backdrop-filter: blur(20px);

  overflow: hidden;
}

/* =========================
   品牌
========================= */

.brand-header {
  position: relative;
  z-index: 5;

  display: flex;
  align-items: center;

  gap: 14px;
}

.brand-logo {
  width: 42px;
  height: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background: rgba(255, 255, 255, 0.08);

  border: 1px solid rgba(255, 255, 255, 0.12);

  box-shadow:
    0 0 30px rgba(59, 130, 246, 0.25);
}

.brand-logo img {
  width: 28px;
  height: 28px;

  border-radius: 7px;
}

.brand-name {
  font-size: 18px;
  font-weight: 700;

  letter-spacing: 0.08em;
}

.brand-subtitle {
  margin-top: 3px;

  color: #64748b;

  font-size: 9px;

  letter-spacing: 0.2em;
}

/* =========================
   中央视觉
========================= */

.visual-area {
  position: relative;

  width: 430px;
  height: 430px;

  margin: auto;

  display: flex;
  align-items: center;
  justify-content: center;
}

/* 环 */
.orbit {
  position: absolute;

  border-radius: 50%;

  border: 1px solid rgba(96, 165, 250, 0.15);

  animation: rotate 20s linear infinite;
}

.orbit-one {
  width: 260px;
  height: 260px;
}

.orbit-two {
  width: 340px;
  height: 340px;

  border-color: rgba(139, 92, 246, 0.15);

  animation-duration: 28s;

  animation-direction: reverse;
}

.orbit-three {
  width: 420px;
  height: 420px;

  border-color: rgba(14, 165, 233, 0.08);

  animation-duration: 40s;
}

/* 中心 */
.core {
  position: relative;

  width: 150px;
  height: 150px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(59, 130, 246, 0.3),
      rgba(15, 23, 42, 0.8) 65%
    );

  box-shadow:
    0 0 50px rgba(59, 130, 246, 0.3),
    inset 0 0 40px rgba(59, 130, 246, 0.15);
}

.core-inner {
  width: 80px;
  height: 80px;

  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;

  background: rgba(15, 23, 42, 0.9);

  border: 1px solid rgba(96, 165, 250, 0.5);

  box-shadow:
    0 0 30px rgba(59, 130, 246, 0.5);

  font-size: 22px;

  font-weight: 700;

  color: #60a5fa;

  letter-spacing: 0.1em;
}

.core-ring {
  position: absolute;

  inset: -10px;

  border-radius: 50%;

  border: 1px solid rgba(96, 165, 250, 0.4);

  animation: pulse 2s ease-in-out infinite;
}

/* =========================
   粒子
========================= */

.particle {
  position: absolute;

  width: 3px;
  height: 3px;

  border-radius: 50%;

  background: #60a5fa;

  box-shadow:
    0 0 8px #60a5fa;

  animation: particleFloat 4s ease-in-out infinite;
}

/* =========================
   左下
========================= */

.brand-footer {
  position: relative;
  z-index: 5;

  display: flex;
  gap: 10px;

  color: #475569;

  font-size: 9px;

  letter-spacing: 0.2em;
}

/* =========================
   右侧
========================= */

.login-panel {
  position: relative;
  z-index: 2;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 40px;

  background: rgba(2, 6, 23, 0.72);

  backdrop-filter: blur(20px);
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
}

/* =========================
   移动端 Logo
========================= */

.mobile-logo {
  display: none;
}

/* =========================
   Header
========================= */

.login-header {
  text-align: center;

  margin-bottom: 30px;
}

.welcome-label {
  margin-bottom: 10px;

  color: #60a5fa;

  font-size: 10px;

  letter-spacing: 0.25em;

  font-weight: 600;
}

.login-header h1 {
  margin: 0;

  font-size: 30px;

  font-weight: 700;

  letter-spacing: -0.02em;
}

.login-header p {
  margin-top: 10px;

  color: #64748b;

  font-size: 13px;
}

/* =========================
   登录盒子
========================= */

.login-box {
  position: relative;

  padding: 30px;

  border-radius: 18px;

  border: 1px solid rgba(255, 255, 255, 0.08);

  background:
    linear-gradient(
      145deg,
      rgba(255, 255, 255, 0.06),
      rgba(255, 255, 255, 0.025)
    );

  backdrop-filter: blur(25px);

  box-shadow:
    0 25px 80px rgba(0, 0, 0, 0.45),
    inset 0 1px rgba(255, 255, 255, 0.05);

  transition:
    transform 0.4s ease,
    border-color 0.4s ease,
    box-shadow 0.4s ease;
}

/* 鼠标悬停 */

.login-box:hover {
  transform: translateY(-4px);

  border-color: rgba(96, 165, 250, 0.35);

  box-shadow:
    0 30px 90px rgba(0, 0, 0, 0.55),
    0 0 45px rgba(59, 130, 246, 0.1);
}

/* 顶部光线 */

.top-line {
  position: absolute;

  left: 15%;

  top: -1px;

  width: 70%;

  height: 1px;

  background:
    linear-gradient(
      90deg,
      transparent,
      #60a5fa,
      #a78bfa,
      transparent
    );

  box-shadow:
    0 0 15px rgba(96, 165, 250, 0.8);
}

/* =========================
   表单
========================= */

.form-style {
  width: 100%;
}

.input-label {
  margin-bottom: 7px;

  color: #cbd5e1;

  font-size: 12px;

  font-weight: 500;
}

/* Element Plus */

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-input__wrapper) {
  height: 46px;

  padding-left: 13px;

  border-radius: 10px;

  background: rgba(15, 23, 42, 0.75);

  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.07);

  transition:
    all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow:
    0 0 0 1px rgba(96, 165, 250, 0.3);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow:
    0 0 0 1px #3b82f6,
    0 0 20px rgba(59, 130, 246, 0.15);
}

:deep(.el-input__inner) {
  color: #e2e8f0;

  font-size: 13px;
}

:deep(.el-input__inner::placeholder) {
  color: #475569;
}

:deep(.el-input__prefix-inner) {
  color: #64748b;
}

/* =========================
   按钮
========================= */

.btns {
  width: 100%;

  display: flex;

  gap: 10px;
}

.login-btn {
  flex: 1;

  height: 46px;

  border: none;

  border-radius: 10px;

  color: white;

  font-weight: 600;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #7c3aed
    );

  box-shadow:
    0 8px 25px rgba(59, 130, 246, 0.25);

  transition:
    all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);

  box-shadow:
    0 12px 35px rgba(59, 130, 246, 0.4);

  background:
    linear-gradient(
      135deg,
      #3b82f6,
      #8b5cf6
    );
}

.arrow {
  margin-left: 10px;

  transition:
    transform 0.3s ease;
}

.login-btn:hover .arrow {
  transform: translateX(5px);
}

.reset-btn {
  width: 80px;

  height: 46px;

  margin-left: 0;

  border-radius: 10px;

  border: 1px solid rgba(255, 255, 255, 0.08);

  background: rgba(255, 255, 255, 0.04);

  color: #94a3b8;

  transition:
    all 0.3s ease;
}

.reset-btn:hover {
  color: white;

  border-color: rgba(255, 255, 255, 0.2);

  background: rgba(255, 255, 255, 0.08);
}

/* =========================
   状态
========================= */

.system-status {
  margin-top: 20px;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 7px;

  color: #475569;

  font-size: 9px;

  letter-spacing: 0.2em;
}

.status-dot {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #34d399;

  box-shadow:
    0 0 10px #34d399;

  animation: pulse 2s infinite;
}

/* =========================
   Footer
========================= */

.login-footer {
  margin-top: 25px;

  display: flex;

  justify-content: space-between;

  color: #334155;

  font-size: 9px;

  letter-spacing: 0.12em;
}

/* =========================
   动画
========================= */

@keyframes rotate {

  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }

}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);

    opacity: 0.6;
  }

  50% {
    transform: scale(1.08);

    opacity: 1;
  }

}

@keyframes particleFloat {

  0%,
  100% {
    transform: translateY(0);

    opacity: 0.3;
  }

  50% {
    transform: translateY(-15px);

    opacity: 1;
  }

}

/* =========================
   响应式
========================= */

@media (max-width: 900px) {

  .login-container {
    display: block;
  }

  .brand-panel {
    display: none;
  }

  .login-panel {
    min-height: 100vh;

    padding: 25px;
  }

  .mobile-logo {
    display: flex;

    align-items: center;

    justify-content: center;

    gap: 10px;

    margin-bottom: 35px;

    font-weight: 700;

    letter-spacing: 0.08em;
  }

  .mobile-logo img {
    width: 35px;
    height: 35px;

    border-radius: 8px;
  }

}

@media (max-width: 480px) {

  .login-panel {
    padding: 20px;
  }

  .login-box {
    padding: 22px;
  }

  .login-header h1 {
    font-size: 25px;
  }

  .login-footer {
    flex-direction: column;

    align-items: center;

    gap: 6px;
  }

}
</style>
