# dwbCommon.db

## Example

| pkgId | timestamps          | name                     | eventType | eventTypeReadable               |
| ----- | ------------------- | ------------------------ | --------- | ------------------------------- |
| 171   | 2025-06-22 14:08:06 | android                  | 18        | KEYGUARD_HIDDEN (DEVICE UNLOCK) |
| 155   | 2025-06-22 14:08:19 | com.zhiliaoapp.musically | 1         | ACTIVITY_RESUMED                |
| 155   | 2025-06-22 14:09:52 | com.zhiliaoapp.musically | 2         | ACTIVITY_PAUSED                 |
| 155   | 2025-06-22 14:09:52 | com.zhiliaoapp.musically | 23        | ACTIVITY_STOPPED                |
| ...   | ...                 | ...                      | ...       | ...                             |

## References

- https://thebinaryhick.blog/2020/02/22/walking-the-android-timeline-using-androids-digital-wellbeing-to-timeline-android-activity/
- https://developer.android.com/reference/android/app/usage/UsageEvents.Event
- https://developer.android.com/reference/android/app/Activity

