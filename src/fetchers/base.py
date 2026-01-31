"""基础抓取器抽象类"""
import logging
import time
from abc import ABC, abstractmethod
from typing import List, Callable, TypeVar
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry(times: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < times - 1:
                        logger.warning(f"{func.__name__} failed (attempt {attempt + 1}/{times}): {e}")
                        time.sleep(delay * (attempt + 1))
                    else:
                        logger.error(f"{func.__name__} failed after {times} attempts: {e}")
            raise last_exception
        return wrapper
    return decorator


class BaseFetcher(ABC):
    """基础抓取器抽象类"""

    # 优先级：RSS > API > HTML
    FETCH_TYPE = "html"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    @abstractmethod
    def fetch(self, limit: int = 20) -> List:
        """
        抓取资讯

        Args:
            limit: 最多抓取条数

        Returns:
            List[NewsItem]: 资讯列表
        """
        pass

    def _get_source_name(self) -> str:
        """获取来源名称"""
        return self.__class__.__name__.replace("Fetcher", "")

    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        return text.strip().replace("\n", " ").replace("\r", " ").replace("\t", " ")
