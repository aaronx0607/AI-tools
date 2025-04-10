// 监听路由变化并触发自定义事件
function initRouteChangeDetection() {
  // 存储当前路径
  let currentPath = window.location.pathname;
  let currentSearch = window.location.search;
  
  // 定期检查路径是否变化
  const intervalId = setInterval(() => {
    if (currentPath !== window.location.pathname || currentSearch !== window.location.search) {
      // 路径已变化，触发自定义事件
      currentPath = window.location.pathname;
      currentSearch = window.location.search;
      console.log('Route changed to:', currentPath + currentSearch);
      
      // 创建并分发自定义事件
      const event = new CustomEvent('astro:route-change', { 
        detail: { path: currentPath, search: currentSearch } 
      });
      document.dispatchEvent(event);
    }
  }, 100); // 每100毫秒检查一次
  
  // 清理函数
  return () => clearInterval(intervalId);
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', initRouteChangeDetection);

// Astro视图转换后重新初始化
document.addEventListener('astro:page-load', initRouteChangeDetection);

// 确保在页面已经加载的情况下也能正确初始化
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  initRouteChangeDetection();
}
