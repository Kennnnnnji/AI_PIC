package buaa.android.aipic;

import android.app.Application;
import android.content.Context;
import android.os.StrictMode;
import androidx.multidex.MultiDex;
import com.squareup.leakcanary.LeakCanary;
import com.squareup.leakcanary.RefWatcher;
import io.realm.Realm;
import io.realm.RealmConfiguration;
import buaa.android.aipic.gallery.data.Album;
import buaa.android.aipic.gallery.data.HandlingAlbums;

public class MyApplication extends Application {
  private HandlingAlbums albums = null;
  public static Context applicationContext;
  private RefWatcher refWatcher;

  public Album getAlbum() {
    return albums.dispAlbums.size() > 0 ? albums.getCurrentAlbum() : Album.getEmptyAlbum();
  }

  @Override
  public void onCreate() {
    StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
    StrictMode.setVmPolicy(builder.build());

    refWatcher = LeakCanary.install(this);
    albums = new HandlingAlbums(getApplicationContext());
    applicationContext = getApplicationContext();

    MultiDex.install(this);

    Realm.init(this);
    RealmConfiguration realmConfiguration =
        new RealmConfiguration.Builder()
            .name("aipic.realm")
            .schemaVersion(1)
            .deleteRealmIfMigrationNeeded()
            .build();
    Realm.setDefaultConfiguration(realmConfiguration);
    super.onCreate();
  }

  public static RefWatcher getRefWatcher(Context context) {
    MyApplication myApplication = (MyApplication) context.getApplicationContext();
    return myApplication.refWatcher;
  }

  @Override
  protected void attachBaseContext(Context base) {
    super.attachBaseContext(base);
  }

  public HandlingAlbums getAlbums() {
    return albums;
  }
}
