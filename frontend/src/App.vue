<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type User = {
  id: number
  phone: string
  full_name: string
  role: string
  status: string
}

type Mission = {
  id: number
  customer_id: number
  project_id: number
  title: string
  description: string
  required_skills: string[]
  rate: string | number
  start_date: string
  end_date: string
  status: string
  created_at: string
}

type Assignment = {
  id: number
  mission_id: number
  fighter_id: number
  squad_id: number | null
  status: string
}

const token = ref(localStorage.getItem('sanich_token') ?? '')
const user = ref<User | null>(null)
const missions = ref<Mission[]>([])
const myMissions = ref<Mission[]>([])
const message = ref('')
const error = ref('')

const loginPhone = ref('')
const loginPassword = ref('')
const registerPhone = ref('')
const registerName = ref('')
const registerPassword = ref('')
const registerRole = ref('fighter')

const missionTitle = ref('')
const missionDescription = ref('')
const missionProjectId = ref('')
const missionSkills = ref('')
const missionRate = ref('')
const missionStart = ref('')
const missionEnd = ref('')

const loggedIn = computed(() => Boolean(token.value))
const isCustomer = computed(() => user.value?.role === 'customer')
const canApply = computed(() => user.value?.role === 'fighter' || user.value?.role === 'squad_leader')

function clearMessage() {
  message.value = ''
  error.value = ''
}

async function request(path: string, options: RequestInit = {}) {
  clearMessage()

  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')

  if (token.value) {
    headers.set('Authorization', `Bearer ${token.value}`)
  }

  const response = await fetch(`/api${path}`, {
    ...options,
    headers,
  })

  const text = await response.text()
  let data: any = null

  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!response.ok) {
    throw new Error(data?.detail ?? `Ошибка HTTP ${response.status}`)
  }

  return data
}

async function register() {
  try {
    const data = await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        phone: registerPhone.value,
        full_name: registerName.value,
        password: registerPassword.value,
        role: registerRole.value,
      }),
    })

    message.value = `Пользователь создан: ${data.full_name}`
    registerPassword.value = ''
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка регистрации'
  }
}

async function login() {
  try {
    const data = await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        phone: loginPhone.value,
        password: loginPassword.value,
      }),
    })

    token.value = data.access_token
    localStorage.setItem('sanich_token', token.value)
    message.value = 'Вход выполнен'
    await getMe()
    await loadMissions()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка входа'
  }
}

async function getMe() {
  try {
    user.value = await request('/auth/me')
  } catch (e) {
    user.value = null
    error.value = e instanceof Error ? e.message : 'Не удалось получить пользователя'
  }
}

function logout() {
  token.value = ''
  user.value = null
  localStorage.removeItem('sanich_token')
  message.value = 'Вы вышли из аккаунта'
}

async function loadMissions() {
  try {
    missions.value = await request('/missions')
    message.value = `Загружено миссий: ${missions.value.length}`
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось загрузить миссии'
  }
}

async function loadMyMissions() {
  try {
    myMissions.value = await request('/missions/my')
    message.value = `Ваших миссий: ${myMissions.value.length}`
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось загрузить ваши миссии'
  }
}

async function createMission() {
  try {
    const data = await request('/missions', {
      method: 'POST',
      body: JSON.stringify({
        title: missionTitle.value,
        description: missionDescription.value,
        project_id: Number(missionProjectId.value),
        required_skills: missionSkills.value
          .split(',')
          .map((skill) => skill.trim())
          .filter(Boolean),
        rate: Number(missionRate.value),
        start_date: missionStart.value,
        end_date: missionEnd.value,
      }),
    })

    message.value = `Миссия создана: #${data.id}`
    await loadMissions()
    await loadMyMissions()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось создать миссию'
  }
}

async function applyToMission(missionId: number) {
  try {
    const data: Assignment = await request(`/missions/${missionId}/apply`, {
      method: 'POST',
      body: JSON.stringify({}),
    })

    message.value = `Отклик создан: #${data.id}`
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось откликнуться'
  }
}

onMounted(async () => {
  if (token.value) {
    await getMe()
    if (user.value) {
      await loadMissions()
    }
  }
})
</script>

<template>
  <main class="container">
    <header>
      <h1>СанычЪ</h1>
      <p>Простой рабочий фронтенд</p>
    </header>

    <div v-if="message" class="message success">{{ message }}</div>
    <div v-if="error" class="message error">{{ error }}</div>

    <section class="grid">
      <article class="card">
        <h2>Авторизация</h2>
        <input v-model="loginPhone" placeholder="Телефон" />
        <input v-model="loginPassword" type="password" placeholder="Пароль" />
        <button @click="login">Войти</button>
      </article>

      <article class="card">
        <h2>Регистрация</h2>
        <input v-model="registerPhone" placeholder="Телефон" />
        <input v-model="registerName" placeholder="ФИО" />
        <input v-model="registerPassword" type="password" placeholder="Пароль (от 6 символов)" />
        <select v-model="registerRole">
          <option value="fighter">Боец</option>
          <option value="squad_leader">Бригадир</option>
          <option value="customer">Заказчик</option>
        </select>
        <button @click="register">Зарегистрироваться</button>
      </article>
    </section>

    <section class="card">
      <h2>Аккаунт</h2>
      <p v-if="user">
        <b>{{ user.full_name }}</b> · {{ user.phone }} · роль: {{ user.role }} · статус: {{ user.status }}
      </p>
      <p v-else>Пользователь не загружен.</p>
      <div class="buttons">
        <button :disabled="!loggedIn" @click="getMe">Проверить /auth/me</button>
        <button :disabled="!loggedIn" class="secondary" @click="logout">Выйти</button>
      </div>
    </section>

    <section class="card">
      <h2>Открытые миссии</h2>
      <button @click="loadMissions">Обновить список</button>

      <div v-if="missions.length" class="missions">
        <div v-for="mission in missions" :key="mission.id" class="mission">
          <h3>#{{ mission.id }} — {{ mission.title }}</h3>
          <p>{{ mission.description }}</p>
          <p><b>Проект:</b> {{ mission.project_id }} · <b>Ставка:</b> {{ mission.rate }}</p>
          <p><b>Даты:</b> {{ mission.start_date }} — {{ mission.end_date }}</p>
          <p v-if="mission.required_skills.length"><b>Навыки:</b> {{ mission.required_skills.join(', ') }}</p>
          <button v-if="canApply" @click="applyToMission(mission.id)">Откликнуться</button>
        </div>
      </div>
      <p v-else class="muted">Открытых миссий нет.</p>
    </section>

    <section class="card">
      <h2>Мои миссии</h2>
      <button :disabled="!isCustomer" @click="loadMyMissions">Загрузить мои миссии</button>
      <div v-if="myMissions.length" class="missions">
        <div v-for="mission in myMissions" :key="mission.id" class="mission">
          <h3>#{{ mission.id }} — {{ mission.title }}</h3>
          <p>{{ mission.description }}</p>
          <p>{{ mission.start_date }} — {{ mission.end_date }} · {{ mission.rate }}</p>
          <p>Статус: {{ mission.status }}</p>
        </div>
      </div>
    </section>

    <section class="card">
      <h2>Создание миссии</h2>
      <p class="muted">Доступно только заказчику. ID проекта вводится вручную, потому что Project API пока не реализован.</p>
      <input v-model="missionTitle" placeholder="Название" />
      <textarea v-model="missionDescription" placeholder="Описание"></textarea>
      <input v-model="missionProjectId" type="number" min="1" placeholder="ID проекта" />
      <input v-model="missionSkills" placeholder="Навыки через запятую" />
      <input v-model="missionRate" type="number" min="0.01" step="0.01" placeholder="Ставка за смену" />
      <label>Дата начала</label>
      <input v-model="missionStart" type="date" />
      <label>Дата окончания</label>
      <input v-model="missionEnd" type="date" />
      <button :disabled="!isCustomer" @click="createMission">Создать миссию</button>
    </section>
  </main>
</template>
