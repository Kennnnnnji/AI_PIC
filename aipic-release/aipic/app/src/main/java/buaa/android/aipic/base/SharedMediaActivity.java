package buaa.android.aipic.base;

import android.os.Bundle;
import buaa.android.aipic.MyApplication;
import buaa.android.aipic.gallery.data.Album;
import buaa.android.aipic.gallery.data.HandlingAlbums;

/** Created by dnld on 03/08/16. */
public class SharedMediaActivity extends ThemedActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
  }

  public static HandlingAlbums getAlbums() {
    return ((MyApplication) MyApplication.applicationContext).getAlbums();
  }

  public Album getAlbum() {
    return ((MyApplication) getApplicationContext()).getAlbum();
  }
}
