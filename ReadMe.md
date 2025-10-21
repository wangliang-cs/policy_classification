# 政策分类

### 输入格式

```json
[
	{
		"motivation": {
		  "解决官方TabHost体验痛点": "2013 年前后的 Android 官方 TabHost/TabWidget 在滑动、样式定制和 Fragment 嵌套上体验差，Javier Pardo 在开发西班牙本地新闻客户端时反复遇到指示器错位、动画卡顿问题，遂将自写的「可滑动 + 完全自定义样式」的 TabStrip 抽取成库，降低自己及社区同类应用的开发成本。",
		  "提升个人技术品牌与欧州Android社区影响力": "作为独立开发者，Javier 通过开源可立即感见的 UI 组件快速积累 GitHub 关注，为后续承接技术顾问、演讲（如 2014 年 Droidcon Madrid）创造名片效应，同时填补西班牙裔开发者在 Android UI 方向缺少明星项目的空白。",
		  "Material Design早期红利": "2013-2014 Google 力推 Material Design，开发者急需符合新设计规范（滑动指示器、波纹、调色板）的现成控件。PagerSlidingTabStrip 率先内置调色板取色 API 和波浪动画，帮助 Javier 抢占 MD 生态早期流量入口。",
		  "商业项目复用与维护成本最小化": "库本身源自其承接的多个外包 App，通过开源让外部开发者共同测试/PR，Javier 将维护成本转嫁给社区，同时保证自用项目持续获得最新兼容补丁，形成“自用⇄开源”闭环。},"
		},
		"policy": {
		  "有利政策": {
			"Google I/O 2014 正式发布 Material Design规范": {
			  "发布时间": "2014-06-25",
			  "政策内容和影响": "规范提出固定/滚动 Tab 模式、强调滑动指示器与配色一致性；PagerSlidingTabStrip 迅速发布 1.0.1 版本增加 palette 取色与波纹选中动画，顺势成为早期 MD 教程里的推荐第三方控件，Star 数出现陡峭增长。",
			  "引用": "https://www.youtube.com/watch?v=KQxH8KTql0Y&t=1280s"
			},
			"Android Support Library 22.1 公开TabLayout预览代码": {
			  "发布时间": "2015-03-20",
			  "政策内容和影响": "Google 虽放出官方 TabLayout，但当时仅支持 Support Library 22.1+，对 4.x 设备兼容要求高；PagerSlidingTabStrip 反向发布兼容 2.3 的 1.0.8 版本，继续承接老项目与不愿升级 Support 库的企业需求，延长生命周期。",
			  "引用": "https://android-developers.googleblog.com/2015/05/android-design-support-library.html"
			},
			"AOSP Apache 2.0 宽松许可证推广": {
			  "发布时间": "2011-11 起持续",
			  "政策内容和影响": "Google 官方文档长期鼓励使用 Apache-2.0。PagerSlidingTabStrip 采用同一许可证，企业可闭源商用；大量 SDK 与外包团队直接内嵌该库，加速传播。",
			  "引用": "https://source.android.com/docs/setup/about/licenses"
			}
		  },
		  "不利政策": {
			"Google 2015 I/O 发布官方TabLayout并纳入Design Support Library": {
			  "发布时间": "2015-05-28",
			  "政策内容和影响": "官方控件与 ViewPager 深度集成、自带 MD 动画并受 AndroidX 长期维护，社区教程全面转向 TabLayout；PagerSlidingTabStrip 新增 Star 断崖式下跌，Javier 在 issue #227 中承认「官方已覆盖 90% 需求」，项目进入维护模式。",
			  "引用": "https://developer.android.com/reference/com/google/android/material/tabs/TabLayout"
			},
			"Google Play 2018 收紧 TargetSdkVersion 政策": {
			  "发布时间": "2018-12-07",
			  "政策内容和影响": "Play 要求 2019-11 起新应用 targetSdk≥28；库最后一次大规模 commit 停留在 2016，未适配 28 以上私有 API 限制与 ViewPager2，导致新上架项目若引用则会被拒绝或警告，社区 Fork 激增而主仓库活跃度归零。",
			  "引用": "https://support.google.com/googleplay/android-developer/answer/113469#targetsdkversion"
			},
			"AndroidX 强制迁移": {
			  "发布时间": "2018-05-08",
			  "政策内容和影响": "Google 停止 Support Library 更新并推出 AndroidX；PagerSlidingTabStrip 仍基于 support-v4，开发者需自行 jetifier 或 Fork 才能在新项目使用，进一步加速用户流失。",
			  "引用": "https://developer.android.com/jetpack/androidx/migrate"
			}
		  }
		},
		"technology": {
		  "新技术刺激": {
			"Material Design 设计语言": {
			  "技术/标准内容+推动库新增的功能及价值": "MD 强调「滑动指示器+Palette 动态取色」；库在 v1.0.1 新增 setIndicatorColorResource() 与 PagerSlidingTabStrip(Context,AttributeSet,int defStyleAttr) 构造，支持直接绑定 Palette 生成色值，实现「状态栏/导航栏/指示器」同色一体化，成为早期 MD 开源示范案例。"
			},
			"ViewPager2 + RecyclerView 架构": {
			  "技术/标准内容+推动库新增的功能及价值": "2019 年 ViewPager2 基于 RecyclerView 重写，要求 Adapter 实现 FragmentStateAdapter；原库耦合旧 PagerAdapter，社区出现多条「ViewPager2 兼容」PR（#248、#259），但作者已停止维护，凸显技术换代对旧库的淘汰效应。"
			},
			"Android Gradle Plugin 3.0+ 静态资源优化": {
			  "技术/标准内容+推动库新增的功能及价值": "AGP 3.0 引入 aapt2 与资源缩减；库早期使用反射获取 R 颜色值导致 R 类被裁剪后崩溃，作者在 v1.0.12 改为 Resources#getColor() 并增加 consumerProguardRules，示范了第三方库适配构建工具链的典型过程。"
			}
		  },
		  "技术演化": {
			"Android Support Library → AndroidX 迁移": {
			  "技术/平台迭代内容+库的适配动作及影响": "原依赖 support-v4:22+；AndroidX 重构包名后主仓库未跟进，社区 Fork（如 psl/PagerSlidingTabStrip-AndroidX）自行迁移，主项目因此丧失官方唯一入口，加速边缘化。"
			},
			"Android 6.0 运行时权限与悬浮窗限制": {
			  "技术/平台迭代内容+库的适配动作及影响": "API23 起悬浮窗需 SYSTEM_ALERT_WINDOW 权限；库早期 demo 用悬浮窗展示样式，新版 demo 改为常规 Activity，避免在 6.0 设备因权限缺失崩溃，体现对系统权限模型的被动适配。"
			},
			"Android 10 Scoped Storage": {
			  "技术/平台迭代内容+库的适配动作及影响": "API29 默认分区存储，与库本身无直接关联，但其 sample 中保存截图到外部存储逻辑失效；社区 issue #266 提出兼容方案，反映即使 UI 控件库也需随系统存储模型更新 demo。"
			}
		  }
		},
		"licenseComment": "采用 Apache-2.0，允许闭源商用且无需开源衍生代码，使大量商业 App（含出海西班牙语区应用）可直接内嵌；宽松条款降低法务审查成本，是 2013-2016 年快速传播的关键助推器之一。",
		"repo": "github:jpardogo/PagerSlidingTabStrip"
	  },
	  {
		"motivation": {
		  "填补Compose Multiplatform动态主题空白": "2023年Google尚未将Jetpack Compose的Material You动态取色（dynamic color）移植到Compose Multiplatform，跨平台Flutter/Dart与Kotlin/React Native开发者缺乏官方方案，Jordon de Hoog通过封装Material Design 3的color-utility算法，提供单一代码库即可在Android/iOS/Desktop生成动态调色板，满足其个人及客户项目“一套UI、多端一致”需求。",
		  "个人品牌与咨询业务增值": "作者在加拿大经营独立APP与UI咨询，开源MaterialKolor可直接展示其对Material Design 3与Kotlin Multiplatform的深度实践，吸引跨平台外包订单，同时通过GitHub Sponsor与BuyMeACoffee获得持续捐赠，形成“技术影响力→客户线索→商业收入”闭环。",
		  "生态贡献与社区回馈": "作者长期活跃于Kotlin Slack与r/FlutterDev，自述“喜欢把Google的私有API搬到开源世界”，在2022-2023年已发布多个Compose扩展库；MaterialKolor延续其“让Compose everywhere”理念，快速收获社区Star与PR，强化其在Kotlin生态的KOL地位。}"
		},
		"policy": {
		  "有利政策": {
			"Google 发布 Material You 动态取色指南（2021-10-28）": {
			  "发布时间": "2021-10-28",
			  "政策内容和影响": "Google将Material You动态颜色列为Android 12+官方设计规范并开源color-utility算法，MaterialKolor直接复用该算法实现跨平台移植，节省逆向成本并确保与官方效果一致。",
			  "引用": "https://github.com/material-foundation/material-color-utilities"
			},
			"Kotlin Multiplatform进入Beta（2022-12-08）": {
			  "发布时间": "2022-12-08",
			  "政策内容和影响": "JetBrains宣布KMP进入Beta并提供稳定二进制接口，MaterialKolor在2023-08立项时即采用KMP结构，可在iOS/macOS目标输出Swift-compatible框架，扩大潜在用户群。",
			  "引用": "https://blog.jetbrains.com/kotlin/2022/12/kotlin-multiplatform-beta/"
			}
		  },
		  "不利政策": {
			"Apple App Store 2.5.2 对“非原生UI”审查趋严（2023-04）": {
			  "发布时间": "2023-04",
			  "政策内容和影响": "部分开发者反馈使用Flutter/Compose Multiplatform的App因“外观不符合iOS Human Interface Guideline”被驳回，MaterialKolor默认生成Material 3调色板，需额外提供iOS适配示例（ tonal-spot → iOS 13 color palette 映射）以降低被拒风险。",
			  "引用": "https://developer.apple.com/forums/thread/728021"
			},
			"Google Play 17.0.0 限制无障碍服务（2022-12-13）": {
			  "发布时间": "2022-12-13",
			  "政策内容和影响": "政策禁止调用无障碍API实现非无障碍功能，与MaterialKolor无关，但间接导致动态主题类库不能再通过无障碍服务抓取壁纸主色，MaterialKolor改为使用WallpaperManager API，需开发者声明READ_EXTERNAL_STORAGE权限，增加集成复杂度。",
			  "引用": "https://support.google.com/googleplay/android-developer/answer/10964491"
			}
		  }
		},
		"technology": {
		  "新技术刺激": {
			"Material Design 3 Color System（2021-10）": "提供基于CAM16色貌模型的量化算法，MaterialKolor将其移植为Kotlin Common代码，使非Android平台也能生成Tonal Spot、Vibrant等五套官方色彩方案，提升跨平台App的视觉一致性。",
			"Jetpack Compose 1.5 引入 ColorScheme 自动生成API（2023-07）": "Google在compose-material3:1.1.0中新增dynamicDarkColorScheme/dynamicLightColorScheme，MaterialKolor在1.3.0版本同步封装对应接口，并扩展支持iOS/macOS通过NSColor/UIColor直接生成Compose ColorScheme，减少平台差异胶水代码。"
		  },
		  "技术演化": {
			"Kotlin Multiplatform 1.9 默认启用新版内存模型（2023-07）": "解除旧内存模型的冻结限制，MaterialKolor在1.2.0起将调色板生成逻辑放入CommonMain，无需再写expect/actual，性能提升约18%，并支持在Swift中同步调用，提高iOS端集成体验。",
			"Flutter 3.16 内置 Material 3 动态取色（2023-11）": "官方通过dynamic_color插件提供Android动态色，MaterialKolor针对iOS/Desktop空白场景，新增createFlutterColorScheme()扩展，输出Flutter ColorScheme JSON，使Flutter开发者可在iOS侧实现与Android一致的动态主题，形成差异化互补。"
		  }
		},
		"repo": "github:jordond/MaterialKolor"
	  }
]
```


### 输出格式

```json
{"repo": "github:adcolony/adcolony-android-sdk", "policy_type": "不利政策", "event": "Google 限制后台启动前台服务（Target-S-Policy）", "policy_content": {"发布时间": "2022-04", "政策内容和影响": "Android 12限制后台应用启动前台服务，AdColony SDK旧版在后台预缓存视频时触发系统ANR/崩溃；4.8.0紧急将缓存任务迁移到WorkManager+DownloadManager，增加集成复杂度并降低预加载成功率。", "引用": "https://developer.android.com/guide/components/foreground-services#background-start-restrictions"}, "policy_category": "应用审核与发布限制"}
```