package com.example.agoravoice;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import io.agora.rtc2.ChannelMediaOptions;
import io.agora.rtc2.Constants;
import io.agora.rtc2.IRtcEngineEventHandler;
import io.agora.rtc2.RtcEngine;
import io.agora.rtc2.RtcEngineConfig;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_REQ_ID = 22;
    private final String appId = "ВАШ_APP_ID";
    private final String channelName = "test_call_channel";  // можно генерировать динамически, например "call_user123_user456"
    private final String token = "ВАШ_TOKEN";               // временный из консоли Agora

    private RtcEngine mRtcEngine;

    private final IRtcEngineEventHandler mRtcEventHandler = new IRtcEngineEventHandler() {
        @Override
        public void onJoinChannelSuccess(String channel, int uid, int elapsed) {
            showToast("Подключились к каналу: " + channel);
        }

        @Override
        public void onUserJoined(int uid, int elapsed) {
            showToast("Собеседник подключился: " + uid);
        }

        @Override
        public void onUserOffline(int uid, int reason) {
            showToast("Собеседник отключился: " + uid);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);  // создайте простой layout с кнопками Join/Leave/Mute

        if (checkSelfPermission()) {
            initializeAndJoinChannel();
        } else {
            requestPermissions();
        }
    }

    private boolean checkSelfPermission() {
        String[] permissions = getRequiredPermissions();
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    private String[] getRequiredPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            return new String[]{Manifest.permission.RECORD_AUDIO, Manifest.permission.READ_PHONE_STATE, Manifest.permission.BLUETOOTH_CONNECT};
        } else {
            return new String[]{Manifest.permission.RECORD_AUDIO};
        }
    }

    private void requestPermissions() {
        ActivityCompat.requestPermissions(this, getRequiredPermissions(), PERMISSION_REQ_ID);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQ_ID && grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            initializeAndJoinChannel();
        }
    }

    private void initializeAndJoinChannel() {
        try {
            RtcEngineConfig config = new RtcEngineConfig();
            config.mContext = getApplicationContext();
            config.mAppId = appId;
            config.mEventHandler = mRtcEventHandler;
            mRtcEngine = RtcEngine.create(config);

            ChannelMediaOptions options = new ChannelMediaOptions();
            options.clientRoleType = Constants.CLIENT_ROLE_BROADCASTER;
            options.channelProfile = Constants.CHANNEL_PROFILE_COMMUNICATION;
            options.publishMicrophoneTrack = true;

            mRtcEngine.joinChannel(token, channelName, 0, options);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void showToast(String message) {
        runOnUiThread(() -> Toast.makeText(this, message, Toast.LENGTH_SHORT).show());
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mRtcEngine != null) {
            mRtcEngine.leaveChannel();
            mRtcEngine = null;
        }
    }

    // Дополнительные методы: mute, leave и т.д.
    public void muteLocalAudio(boolean muted) {
        if (mRtcEngine != null) mRtcEngine.muteLocalAudioStream(muted);
    }
}