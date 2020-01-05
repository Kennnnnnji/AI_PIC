package buaa.android.aipic.utilities;

import buaa.android.aipic.share.imgur.ImgurPicUploadReq;
import buaa.android.aipic.share.imgur.ImgurPicUploadResp;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Header;
import retrofit2.http.POST;

public interface ImgurApi {

  @POST("/image")
  Call<ImgurPicUploadResp> uploadImageToImgur(
      @Header("Authorization") String authorization, @Body ImgurPicUploadReq body);
}
