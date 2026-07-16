export function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ko-KR')
}
