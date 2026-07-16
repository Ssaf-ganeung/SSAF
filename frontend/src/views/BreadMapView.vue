<script setup>
import { computed, ref, watch } from 'vue'

import courseData from '../data/bakeryCourse.json'
import DayTabs from '../components/breadMap/DayTabs.vue'
import CourseMap from '../components/breadMap/CourseMap.vue'
import CourseList from '../components/breadMap/CourseList.vue'

const days = courseData.days

const currentDay = ref(1)
const selectedOrder = ref(null)

const currentCourse = computed(
  () => days.find((d) => d.day === currentDay.value) ?? days[0],
)

// day 전환 시 선택 초기화
watch(currentDay, () => {
  selectedOrder.value = null
})
</script>

<template>
  <div class="bread-map">
    <header class="bread-map__header">
      <h1 class="bread-map__title">🥐 대전 빵지순례</h1>
      <p class="bread-map__subtitle">
        대전의 이름난 빵집을 순서대로 도는 1박 2일 코스를 소개합니다. 지도의
        번호 핀을 눌러 장소 정보를 확인하세요.
      </p>
    </header>

    <DayTabs v-model="currentDay" :days="days" />

    <div class="bread-map__content">
      <section class="bread-map__map" aria-label="코스 지도">
        <CourseMap
          :stops="currentCourse.stops"
          :selected-order="selectedOrder"
          @select="selectedOrder = $event"
        />
      </section>

      <section class="bread-map__list" aria-label="코스 목록">
        <h2 class="bread-map__list-title">{{ currentCourse.title }}</h2>
        <CourseList
          :stops="currentCourse.stops"
          :selected-order="selectedOrder"
          @select="selectedOrder = $event"
        />
      </section>
    </div>
  </div>
</template>

<style scoped>
.bread-map {
  max-width: 1080px;
  margin: 0 auto;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.bread-map__header {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.bread-map__title {
  font-size: var(--font-size-h1);
}

.bread-map__subtitle {
  font-size: var(--font-size-body);
  color: var(--color-text-secondary);
}

.bread-map__content {
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(280px, 2fr);
  gap: 24px;
  align-items: start;
}

.bread-map__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bread-map__list-title {
  font-size: var(--font-size-h3);
}

@media (max-width: 820px) {
  .bread-map {
    padding: 24px 16px;
  }

  /* 모바일: 지도 아래로 리스트 세로 스택 */
  .bread-map__content {
    grid-template-columns: 1fr;
  }
}
</style>
