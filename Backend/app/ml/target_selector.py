from Backend.app.ml import llm

def select_target(llm,objective,columns):

    try:

        prompt = f"""
          you are a ml assistant.

          user objective:
          {objective}
          
           available columns:
           {columns}
            
            identify the column the user want to predict.

            return ONLY the exact column name.
        

        """

        response = llm.invoke(prompt)

        target = response.content.strip()

        if target not in columns:
            raise ValueError(f"invalid target selected:{target}")


        return target


    except Exception as exc:

        raise RuntimeError(f"failed to target selection:{exc}") from exc

    