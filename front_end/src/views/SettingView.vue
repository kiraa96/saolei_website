<template>
    <el-descriptions title="外观设置" :column="3">
        <el-descriptions-item label="语言切换"><el-switch v-model="local.language_show" :active-text="$t('common.show')"
                :inactive-text="$t('common.hide')"></el-switch></el-descriptions-item>
        <el-descriptions-item label="菜单排版"><el-switch v-model="local.menu_icon" active-text="抽象"
                inactive-text="默认"></el-switch></el-descriptions-item>
        <el-descriptions-item label="菜单高度">
            <el-slider v-model="local.menu_height" size="small" :min="20" :max="60" style="width: 100px; display: inline-block; height: 9px"></el-slider>
        </el-descriptions-item>
        <el-descriptions-item label="菜单字号"><el-input-number v-model="local.menu_font_size" size="small" :min="10"/></el-descriptions-item>
        <el-descriptions-item label="通知关闭"><el-tooltip>
            <template #content>
                通知自动关闭的时间，单位毫秒。<br/>值为0则不会自动关闭。
            </template>
            <el-input-number v-model="local.notification_duration" size="small" :min="0" :step="1000"/>
        </el-tooltip></el-descriptions-item>
    </el-descriptions>
    <el-descriptions v-if="store.login_status == LoginStatus.IsLogin" title="个人信息" :column="3">
        <el-descriptions-item label="用户id">{{ store.user.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ store.user.username }}</el-descriptions-item>
        <el-descriptions-item :label="$t('common.prop.realName')">{{ store.user.realname }}</el-descriptions-item>
        <el-descriptions-item label="英文姓">{{ $t('common.toDo') }}</el-descriptions-item>
        <el-descriptions-item label="英文名">{{ $t('common.toDo') }}</el-descriptions-item>
        <el-descriptions-item :label="$t('common.prop.sex')">{{ $t('common.toDo') }}</el-descriptions-item>
        <el-descriptions-item label="属地">{{ $t('common.toDo') }}</el-descriptions-item>
        <el-descriptions-item label="出生年份">{{ $t('common.toDo') }}</el-descriptions-item>
    </el-descriptions>
    <el-descriptions v-if="store.login_status == LoginStatus.IsLogin" title="账号关联">
        <el-table>

        </el-table>
    </el-descriptions>
</template>

<script lang="ts" setup name="UserSettings">

import { useLocalStore, useUserStore } from '@/store';
import { LoginStatus } from '@/utils/common/structInterface';
import { useI18n } from 'vue-i18n';
const store = useUserStore()
const local = useLocalStore()
const t = useI18n()

</script>