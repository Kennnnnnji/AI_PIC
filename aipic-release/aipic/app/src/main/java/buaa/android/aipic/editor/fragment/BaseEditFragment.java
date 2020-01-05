package buaa.android.aipic.editor.fragment;

import android.os.Bundle;
import androidx.fragment.app.Fragment;
import buaa.android.aipic.MyApplication;
import buaa.android.aipic.editor.EditImageActivity;

public abstract class BaseEditFragment extends Fragment {
  protected EditImageActivity activity;

  protected EditImageActivity ensureEditActivity() {
    if (activity == null) {
      activity = (EditImageActivity) getActivity();
    }
    return activity;
  }

  @Override
  public void onActivityCreated(Bundle savedInstanceState) {
    super.onActivityCreated(savedInstanceState);
    ensureEditActivity();
  }

  @Override
  public void onDestroy() {
    super.onDestroy();
    MyApplication.getRefWatcher(getActivity()).watch(this);
  }

  public abstract void onShow();
}
